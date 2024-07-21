# Kafka Streams with Faust

### Streams

Kafka streams são dados ilimitados e contínuos que são gerados em tempo real. Eles são usados para processar dados em tempo real. Kafka

### Tables

Table para Kafka streams é um conceito que permite armazenar o resultado de um stream em um banco de dados. Isso permite que você faça queries sobre o resultado de um stream.

## Stateless Transformations

- Stateless transformations são operações que não dependem do estado anterior. Eles são operações que não dependem de dados anteriores para produzir um resultado.
- Stateless transformations são operações que podem ser aplicadas a cada registro de um stream de forma independente.
- Filter, map, flatMap, etc são exemplos de Stateless transformations.


## Stateful Transformations

- Stateful transformations são operações que dependem do estado anterior. Eles são operações que dependem de dados anteriores para produzir um resultado.
- Precisa ser utilizado junto de um groupBy para garantir que os dados sejam processados em ordem.
- Joins, Reduce, Aggregate and Count são exemplos de Stateful transformations.


### Agents

Event processor responsible for processing events from a Kafka topic.

### Channels

Is an abstraction representing a buffer through which messages are passed to be acted upon by an agent.
Channels can be memory-based or backed by a transport storage technology like Kafka topic.

### Topic

Is a named channel and is backed by Kafka topic.

### Stream

Is an infinite asynchronous interable backed by a channel or topic and operated on by an agent.

