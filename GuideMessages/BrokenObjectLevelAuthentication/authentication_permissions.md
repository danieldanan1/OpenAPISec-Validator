####Broken Object Level Authentication  
**Please add to securitySchemes relevant permissions you defined in global security**  
You can choose method from this link:  https://www.iana.org/assignments/http-authschemes/http-authschemes.xhtml  
As represent below 
```yaml
security:
  - OAuth2:
    - read
    - write
components:
  securitySchemes:
    OAuth2:
      type: oauth2
      flows:
        authorizationCode:
          scopes:
            read: read objects in your account
            write: write objects to your account
```