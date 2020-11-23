* Add GitLab support
    * https://docs.gitlab.com/ee/api/projects.html
        * Create repository: 
        `curl -u test -H "Content-Type:application/json" https://gitlab.com/api/v4/projects -d "{ \"name\": \"test\" }"`
        * Webhook:
            *  POST /projects/:id/hooks
                * Need to query for the project ID after creation