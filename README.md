

# Compacted Topics:


Compacted Topics são tópicos que mantém apenas a última versão de uma chave específica.
Ou seja, se uma chave for atualizada, a versão anterior será removida do tópico.

Compacted Topics são úteis para manter o estado de uma aplicação, como por exemplo,
o saldo de uma conta bancária. Nesse caso, a chave seria o número da conta e o valor.

Para configurar um tópico como compacted use **log.clean.policy=compact**


## Producers


- **key.serializer:** Serializer for key (defaults to a UTF8 serializer)
- **value.serializer:** Serializer for value (defaults to a UTF8 serializer)
- **linger.ms:** batching period in milliseconds 
- **batch.size:** The producer will attempt to batch records together into fewer requests whenever multiple records are being sent to the same partition. This helps performance on both the client and the server. This configuration controls the default batch size in bytes. 

- **acks**: The number of acknowledgments the producer requires the leader to have received before considering a request complete. This controls the durability of records that are sent. The following settings are common:

- **enable.idempotence:** When set to 'true', the producer will ensure that exactly one copy of each message is written in the stream. If 'false', producer retries due to broker failures, etc., may write duplicates of the retried message in the stream. Note that enabling idempotence requires max.in.flight.requests.per.connection to be less than or equal to 5, retries to be greater than 0 and acks must be 'all'. If these values are not explicitly set by the user, suitable values will be chosen. If incompatible values are set, a ConfigException will be thrown.
- **max.in.flight.requests.per.connection:** The maximum number of unacknowledged requests the client will send on a single connection before blocking. Note that if this setting is set to be greater than 1 and there are failed sends, there is a risk of message re-ordering due to retries (i.e., if retries are enabled).
        
- **retries:** Setting a value greater than zero will cause the client to resend any record whose send fails with a potentially transient error. Note that this retry is no different than if the client resent the record upon receiving the error. Allowing retries without setting max.in.flight.requests.per.connection to 1 will potentially change the ordering of records because if two batches are sent to a single partition, and the first fails and is retried but the second succeeds, then the records in the second batch may appear first. Note additionally that produce requests will be failed before the number of retries has been exhausted if the timeout configured by delivery.timeout.ms expires first before successful acknowledgement. Users should generally prefer to leave this config unset and instead use delivery.timeout.ms to control retry behavior.

- **delivery.timeout.ms:** An upper bound on the time to report success or failure after a call to send() returns. This limits the total time that a record will be delayed prior to sending, the time to await acknowledgement from the broker (if expected), and the time allowed for retriable send failures. The producer may report failure to send a record earlier than this config if either an unrecoverable error is encountered, the retries have been exhausted, or the record is added to a batch which reached an earlier delivery expiration deadline. The value of this config should be greater than or equal to the sum of request.timeout.ms and linger.ms.