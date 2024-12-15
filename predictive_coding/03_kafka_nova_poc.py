"""
NOVA - Kafka Implementation POC

This experiment implements a three-layer cognitive architecture. Each layer 
operates at different temporal scales and processing depths.

System Architecture:
-------------------
1. Reactive Layer (50-300ms)
   - Handles immediate responses
   - Minimal processing, quick reflexes

2. Responsive Layer (300-1000ms)
   - Context-aware processing
   - Integrates immediate context

3. Reflective Layer (>1000ms)
   - Learning and adaptation
   - Pattern recognition and long-term learning

Message Flow:
------------
Input → Kafka → [Reactive, Responsive, Reflective] → Kafka → Output

Requirements:
------------
- Docker containers for Kafka and Zookeeper
- confluent-kafka-python client
- Python 3.12+ for async/await support

Docker Setup:
------------
# Remove existing containers if needed
# docker rm -f zookeeper kafka

# Run Zookeeper
docker run -d --name zookeeper \
    -e ZOOKEEPER_CLIENT_PORT=2181 \
    -p 2181:2181 \
    confluentinc/cp-zookeeper:latest

# Run Kafka
docker run -d --name kafka \
    --link zookeeper:zookeeper \
    -p 9092:9092 \
    -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 \
    -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 \
    -e KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=PLAINTEXT:PLAINTEXT \
    -e KAFKA_INTER_BROKER_LISTENER_NAME=PLAINTEXT \
    -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
    confluentinc/cp-kafka:latest
"""

from confluent_kafka import Producer, Consumer
import json
import time
from typing import Dict, Any
import asyncio
import logging


logger = logging.getLogger(__name__)


class KafkaPublishError(Exception):
    """Raised when there is an error publishing messages to Kafka"""

    pass


class NOVALayerError(Exception):
    """Base exception for NOVA layer errors"""

    pass


def timed_process(func):
    """Decorator to add timing information to layer processing"""

    async def wrapper(self, message: Dict[str, Any], *args, **kwargs) -> Dict[str, Any]:
        start_time = time.time()
        try:
            result = await func(self, message, *args, **kwargs)
            end_time = time.time()

            # If result is already a dict, update it; otherwise create new dict
            if isinstance(result, dict):
                result.update(
                    {
                        "start_time": start_time,
                        "end_time": end_time,
                        "processing_duration": end_time - start_time,
                    }
                )
                return result
            else:
                return {
                    "result": result,
                    "start_time": start_time,
                    "end_time": end_time,
                    "processing_duration": end_time - start_time,
                }
        except Exception as e:
            logger.error(
                "Layer processing failed",
                extra={"layer": self.__class__.__name__, "error": str(e)},
                exc_info=True,
            )
            raise NOVALayerError(f"Layer processing failed: {e}") from e

    return wrapper


class NOVALayer:
    """
    Base class for NOVA processing layers.

    Handles Kafka producer/consumer setup and message publishing.
    Each layer inherits from this to implement specific processing logic.

    Args:
        kafka_config (Dict[str, Any]): Kafka configuration parameters
    """

    def __init__(self, kafka_config: Dict[str, Any]):
        # Producer config should exclude consumer-specific settings
        producer_config = {"bootstrap.servers": kafka_config["bootstrap.servers"]}

        # Consumer config can keep all settings
        consumer_config = kafka_config.copy()

        self.producer = Producer(producer_config)
        self.consumer = Consumer(consumer_config)

    def close(self):
        """
        Properly close Kafka resources.
        Should be called when the layer is no longer needed.
        """
        if self.producer:
            self.producer.flush()  # Ensure all messages are sent

        if self.consumer:
            self.consumer.close()

    def __del__(self):
        """Ensure resources are cleaned up when object is garbage collected"""
        try:
            self.close()
        except:
            # Ignore errors during cleanup in destructor
            pass

    def publish(self, topic: str, message: Dict[str, Any]):
        """
        Non-blocking publish to Kafka topic
        """
        try:
            self.producer.produce(
                topic,
                json.dumps(message).encode("utf-8"),
                callback=self.delivery_report,
            )
            self.producer.poll(0)  # Non-blocking poll for callbacks
        except Exception as e:
            logger.error(
                "Failed to publish message to Kafka",
                extra={
                    "topic": topic,
                    "error": str(e),
                    "layer": self.__class__.__name__,
                },
                exc_info=True,
            )
            raise KafkaPublishError(f"Failed to publish message to Kafka: {e}") from e

    def delivery_report(self, err, msg):
        """Callback for Kafka message delivery confirmation"""
        if err is not None:
            logger.error(
                "Message delivery failed",
                extra={
                    "topic": msg.topic(),
                    "error": str(err),
                    "layer": self.__class__.__name__,
                },
            )
            # Note: Can't raise here as it's a callback
            # Consider implementing a message retry mechanism
        else:
            logger.debug(
                "Message delivered successfully",
                extra={"topic": msg.topic(), "layer": self.__class__.__name__},
            )


class ReactiveLayer(NOVALayer):
    """
    Fast response layer (50-100ms)

    Handles immediate responses with minimal processing.
    - Fastest response time
    - Minimal context consideration
    - Basic pattern matching
    """

    @timed_process
    async def process(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Quick processing of immediate responses

        Args:
            message (Dict[str, Any]): Input message to process

        Returns:
            Dict[str, Any]: Processed response
        """
        await asyncio.sleep(0.05)  # 50ms for immediate response
        return {
            "type": "reactive_response",
            "content": f"Quick acknowledgment: {message.get('content', '')}",
        }


class ResponsiveLayer(NOVALayer):
    """
    Context-aware layer (100-300ms)

    Processes information with awareness of immediate context.
    - Medium response time
    - Context integration
    - Short-term pattern recognition
    """

    @timed_process
    async def process(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process with context awareness

        Args:
            message (Dict[str, Any]): Input message to process

        Returns:
            Dict[str, Any]: Context-aware response
        """
        await asyncio.sleep(0.2)  # 200ms for context processing
        return {
            "type": "responsive_response",
            "content": f"Thoughtful response to: {message.get('content', '')}",
            "context": "user_interaction",
        }


class ReflectiveLayer(NOVALayer):
    """
    Learning and adaptation layer (300-500ms)

    Handles pattern learning and long-term adaptation.
    - Pattern analysis
    - Learning and adaptation
    - Long-term memory integration
    """

    @timed_process
    async def process(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process for long-term learning and adaptation

        Args:
            message (Dict[str, Any]): Input message to process

        Returns:
            Dict[str, Any]: Learning/adaptation response
        """
        await asyncio.sleep(0.4)  # 400ms for learning/adaptation
        return {
            "type": "reflective_update",
            "pattern": "user_interaction_pattern",
            "learning": f"Learned from: {message.get('content', '')}",
        }


class NOVA:
    """
    Main NOVA system orchestrator

    Coordinates the three processing layers and handles message distribution.
    Implements parallel processing using asyncio.
    """

    def __init__(self, kafka_config: Dict[str, Any]):
        self.reactive = ReactiveLayer(kafka_config)
        self.responsive = ResponsiveLayer(kafka_config)
        self.reflective = ReflectiveLayer(kafka_config)

    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Process message through all layers in parallel"""
        logger.info("Starting parallel processing", extra={"timestamp": time.time()})

        tasks = {
            "reactive": self.reactive.process(message),
            "responsive": self.responsive.process(message),
            "reflective": self.reflective.process(message),
        }

        results = {}
        for name, task in tasks.items():
            try:
                results[name] = await task
            except Exception as e:
                logger.error(f"Error in {name} layer", exc_info=True)
                results[name] = None

        # Flush producers after all processing
        try:
            for layer in (self.reactive, self.responsive, self.reflective):
                layer.producer.flush()
        except Exception as e:
            logger.error("Failed to flush producers", exc_info=True)
            raise KafkaPublishError("Failed to flush Kafka producers") from e

        logger.info("All processing completed", extra={"timestamp": time.time()})
        return results

    def close(self):
        """Clean up resources for all layers"""
        self.reactive.close()
        self.responsive.close()
        self.reflective.close()

    def __del__(self):
        """Ensure all resources are cleaned up"""
        self.close()


async def main():
    """
    Example usage of the NOVA system

    Sets up Kafka configuration and processes a test message
    through all layers.
    """
    try:
        # Kafka configuration
        kafka_config = {
            "bootstrap.servers": "localhost:9092",
            "group.id": "nova_group",
            "auto.offset.reset": "earliest",
        }

        # Initialize NOVA
        nova = NOVA(kafka_config)

        # Example message
        message = {
            "type": "user_input",
            "content": "Hello, how are you?",
            "timestamp": time.time(),
        }

        # Process message
        results = await nova.process_message(message)
        print("\nProcessing Results:")
        print("Reactive:\n", results["reactive"])
        print("Responsive:\n", results["responsive"])
        print("Reflective:\n", results["reflective"])

    finally:
        # Ensure resources are properly cleaned up
        nova.close()


if __name__ == "__main__":
    asyncio.run(main())
