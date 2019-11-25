# ReDup

>  Repository Duplication

This application produces an URL to an application.
The application behind the URL requests access to the user's GitHub profile and creates
a repository with its own (application's) code.
The application does not ask for the users's password or require access to user's private repositories.

## What could be improved
Due to time limitations, only essential functionality was implemented.

At the current state there are lot of improvements that can be done. Here are some of them:

1. Use "code" GitHub parameter in authentication part.
2. Use specific GitHub API libraries: [RAuth](https://github.com/litl/rauth), [Authomatic](https://authomatic.github.io/authomatic/index.html).
3. User OAuth libraries with GitHub provider support: [AuthLib](https://github.com/lepture/authlib), [requests-oauthlib](https://requests-oauthlib.readthedocs.io/en/latest/).
4. Release each lambda as a wheel package.
5. Implement storing tokens received from GItHub.
6. It is tempting to get rid of only "requests" lib for callback lambda and use urllib3. This way deployment size can be reduced.
7. Create separate lambda for repository creation and link it with callback function via SNS or SQS.
8. Create hosting for front-end part of application and leverage static content distribution via CDN.
9. Authorization/Authentication.
10. Filter dependencies for zip, to reduce lambda size
11. Staging environment



## Team

> Andrii Gryshchenko


 [![Andrii](https://avatars1.githubusercontent.com/u/43616610?s=260)]() 

---

## License

[![License](https://www.gnu.org/graphics/gplv3-127x51.png)](https://opensource.org/licenses/GPL-3.0)

- **[GPL-3.0 license](LICENSE)**

- Copyright 2019 © Andrii Gryshchenko