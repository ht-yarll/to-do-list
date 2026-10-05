# Short Answers

1. How would you configure Coolify to auto-deploy on every push to main, and how would you roll back a bad deploy?
    First I would connect Coolify with my Git repository using a webhook via CI/CD, or an native integration if available on the git service, setting it up so the application is automatically deployed from `main`. Each deployment must have an immutable image tag or a unique identifier. If a deployment goes bad I would redeploy the previous working commit or image and check wether database migration is compatible with the rollback

2. If the server died right now, what are the steps to get the app back online and roughly how long would
it take? Describe Plan A (same server) and Plan B (new server).
    Plan A: If the same server is recoverable, I would inspect the server and application logs, restart the affected services, and roll back to the last known-good release. This could take approximately 15–60 minutes.
    Plan B: If the server cannot be recovered, I would provision a new VPS, install Coolify, restore secrets and configuration, restore the database and persistent storage from tested backups, deploy the last stable version, verify the application, and update DNS. This could take approximately 1–4 hours, depending on the backup and DNS setup.

3. A Linux VPS feels slow or misconfigured. List the first 3–5 things you would check.
    Container status and health: crashes, restart loops, unhealthy checks.
    CPU and memory usage.
    Disk space, inodes, and disk I/O.
    System, application, and logs.
    Network traffic, connection limits, and load-balancer status if applicable.
