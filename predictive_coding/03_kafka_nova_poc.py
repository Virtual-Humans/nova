"""
NOVA (Neural Oscillation Virtual Architecture) - Kafka Implementation POC

This experiment implements a three-layer cognitive architecture inspired by 
predictive processing and neural oscillation patterns in the brain. Each layer 
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
- Python 3.7+ for async/await support

Docker Setup:
------------
# Remove existing containers if needed
# docker rm -f zookeeper kafka

# Run Zookeeper
# docker run -d --name zookeeper \
#     -e ZOOKEEPER_CLIENT_PORT=2181 \
#     -p 2181:2181 \
#     confluentinc/cp-zookeeper:latest

# Run Kafka
# docker run -d --name kafka \
#     --link zookeeper:zookeeper \
#     -p 9092:9092 \
#     -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 \
#     -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 \
#     -e KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=PLAINTEXT:PLAINTEXT \
#     -e KAFKA_INTER_BROKER_LISTENER_NAME=PLAINTEXT \
#     -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
#     confluentinc/cp-kafka:latest
"""

from confluent_kafka import Producer, Consumer
import json
import time
from typing import Dict, Any
import asyncio


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

    def publish(self, topic: str, message: Dict[str, Any]):
        """
        Publish message to a Kafka topic.
        
        Args:
            topic (str): Kafka topic to publish to
            message (Dict[str, Any]): Message content in dictionary format
        """
        try:
            self.producer.produce(
                topic,
                json.dumps(message).encode("utf-8"),
                callback=self.delivery_report,
            )
            self.producer.flush()
        except Exception as e:
            print(f"Error producing message: {e}")

    def delivery_report(self, err, msg):
        """Callback for Kafka message delivery confirmation"""
        if err is not None:
            print(f"Message delivery failed: {err}")
        else:
            print(f"Message delivered to {msg.topic()}")


class ReactiveLayer(NOVALayer):
    """
    Fast response layer (50-300ms)
    
    Handles immediate responses with minimal processing.
    Similar to gamma wave processing in the brain.
    
    Processing characteristics:
    - Fastest response time
    - Minimal context consideration
    - Basic pattern matching
    """

    def process(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Quick processing of immediate responses
        
        Args:
            message (Dict[str, Any]): Input message to process
            
        Returns:
            Dict[str, Any]: Processed response
        """
        # Simulate gamma-wave processing time
        time.sleep(0.1)  # 100ms

        response = {
            "type": "reactive_response",
            "content": f"Quick acknowledgment: {message.get('content', '')}",
            "timestamp": time.time(),
        }

        self.publish("nova.reactive.output", response)
        return response


class ResponsiveLayer(NOVALayer):
    """
    Context-aware layer (300-1000ms)
    
    Processes information with awareness of immediate context.
    Similar to beta wave processing in the brain.
    
    Processing characteristics:
    - Medium response time
    - Context integration
    - Short-term pattern recognition
    """

    def process(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process with context awareness
        
        Args:
            message (Dict[str, Any]): Input message to process
            
        Returns:
            Dict[str, Any]: Context-aware response
        """
        # Simulate beta-wave processing time
        time.sleep(0.3)  # 300ms

        response = {
            "type": "responsive_response",
            "content": f"Thoughtful response to: {message.get('content', '')}",
            "context": "user_interaction",
            "timestamp": time.time(),
        }

        self.publish("nova.responsive.output", response)
        return response


class ReflectiveLayer(NOVALayer):
    """
    Learning and adaptation layer (background processing)
    
    Handles pattern learning and long-term adaptation.
    Similar to alpha/theta wave processing in the brain.
    
    Processing characteristics:
    - Slowest response time
    - Deep pattern analysis
    - Learning and adaptation
    """

    def process(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process for long-term learning and adaptation
        
        Args:
            message (Dict[str, Any]): Input message to process
            
        Returns:
            Dict[str, Any]: Learning/adaptation response
        """
        # Simulate alpha/theta-wave processing time
        time.sleep(0.5)  # 500ms

        response = {
            "type": "reflective_update",
            "pattern": "user_interaction_pattern",
            "learning": f"Learned from: {message.get('content', '')}",
            "timestamp": time.time(),
        }

        self.publish("nova.reflective.output", response)
        return response


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

    async def process_message(self, message: Dict[str, Any]):
        """
        Process message through all layers asynchronously
        
        Creates parallel tasks for each layer and waits for all results.
        
        Args:
            message (Dict[str, Any]): Input message to process
            
        Returns:
            Dict[str, Any]: Combined results from all layers
        """
        # Create tasks for each layer
        reactive_task = asyncio.create_task(
            asyncio.to_thread(self.reactive.process, message)
        )
        responsive_task = asyncio.create_task(
            asyncio.to_thread(self.responsive.process, message)
        )
        reflective_task = asyncio.create_task(
            asyncio.to_thread(self.reflective.process, message)
        )

        # Wait for all tasks to complete
        results = await asyncio.gather(reactive_task, responsive_task, reflective_task)

        return {
            "reactive": results[0],
            "responsive": results[1],
            "reflective": results[2],
        }


async def main():
    """
    Example usage of the NOVA system
    
    Sets up Kafka configuration and processes a test message
    through all layers.
    """
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


if __name__ == "__main__":
    asyncio.run(main())
