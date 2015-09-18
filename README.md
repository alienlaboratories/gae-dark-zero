# gae-dark-zero


## Set-up Push Endpoint

- <https://cloud.google.com/pubsub/prereqs#push_endpoints>
- <https://cloud.google.com/pubsub/libraries#libraries>
- <https://cloud.google.com/pubsub/prereqs#push_endpoints>


### Third-party libs

- <https://cloud.google.com/appengine/docs/python/tools/libraries27#vendoring>

- Pip requires simple hack to work with GAE:

    - <http://stackoverflow.com/questions/24257803/distutilsoptionerror-must-supply-either-home-or-prefix-exec-prefix-not-both>    
    
    echo -e '[install]\nprefix=' >  ~/.pydistutils.cfg 

    sudo -H pip install -t lib --upgrade -r requirements.txt


### Testing

    gcloud preview app run app.yaml


### Deploy

    gcloud preview app deploy --set-default -q app.yaml

