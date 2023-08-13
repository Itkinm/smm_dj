A tool I made for the political campaign I worked for.
It allowed the employees at the headquorters responsible for public messaging to conviniently monitor what 50+ regional offices were posting on 8 different social media channels. It monitored the feeds (some through official APIs some through scraping) and posted the aggregated feed into dedicated Telegram channels. The monitored and the resulting feeds could be fully managed through the Django Admin.
It also aggregated statistics and published them on dedicated webpages using Google Data Studio. 
I used nginx, supervisor and uwsgi to deploy and celery to run recurring tasks. 
