

### Services
The most important services here are `api` and `payment`, the first one provide two endpoints `/api/v1/claim` and `/api/v1/providers`, the second one is a consumer of the provider net fee. The remining services(db, redis pgweb) are helper of these two.

### Running
In order to get all running, we can take advantage of Docker 

```sh
docker compose up
```

### Endpoints
As we mentioned the previous endpoints can be used in the swagger page `/docs`, using the http file included in this project(REST Client extension for VSCode) or any other http client. The right payload are avialable in the `http/claims.http` file.

## Solution pruposed for the communication of claim_process and payment services
We have included a pubsub approach for addressing the communication issue between both services

API <-> Publisher <-> PubSub <-> Consumer <-> Payment

By the time a new calculation happen in the `claim_process` service, a new messages is pushed to the `payment` service. We have used Redis as a broker but it can be replaced by GCP PubSub or a different stack.

### Workaround
Taking advantage of a tech like Kafka can be a good option as well, Kafka allows keep the data in the right queues, in case of a resend or a retry of the information.