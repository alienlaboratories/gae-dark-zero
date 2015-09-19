# gae-dark-zero


## Set-up Push Endpoint

- <https://cloud.google.com/pubsub/prereqs#push_endpoints>
- <https://cloud.google.com/pubsub/libraries#libraries>
- <https://cloud.google.com/pubsub/prereqs#push_endpoints>


### Third-party libs

- <https://cloud.google.com/appengine/docs/python/tools/libraries27#vendoring>

    grunt nx --init
    
    gcloud auth login
    gcloud config set project dark-zero    


### Testing

    gcloud preview app run app.yaml


### Deploy

    gcloud preview app deploy --set-default -q app.yaml

