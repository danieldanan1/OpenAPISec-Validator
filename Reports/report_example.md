
### Loaction: components.securitySchemes.OAuth2
####Broken Object Level Authentication  
Please add security method as value of "OAuth2" under components/securitySchemes a already defined   
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
### Loaction: components.securitySchemes.OAuth2.type
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