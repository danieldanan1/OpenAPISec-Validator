####Broken Object Level Authentication  
**Please add security method as value of "type" key**  
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
```