for deploy to production 
here is my server

here is my main domain manooch.site

the portal app should be deployed on portal.manooch.site
the backend app should be deployed on api.manooch.site
the admin app should be deployed on admin.manooch.site
the website app should be deployed on manooch.site
the cms app should be deployed on cms.manooch.site
the storefront app should be deployed on [storeName].manooch.site (i dont know its possible to dont confilict with other api , admin , cms , portal subdomain)

i set for each repo (manooch-backend , manooch-fronts , manooch-cms) github secrets


i want deploy with git pipline first run workflows then add sercerts to github to deploy each app on my server effect@ubuntu---1-vcpu---2-gb-ram:~/manooch$ dir
and  here is effect@ubuntu---1-vcpu---2-gb-ram:~/manooch$ ls
manooch-backend  manooch-cms  manooch-fronts each repo

and i want my project being dockerize & up & run with docker give me plan to config all envs & all needed to deploy these repo
