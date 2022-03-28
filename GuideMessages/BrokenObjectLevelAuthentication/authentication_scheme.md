####Broken Object Level Authentication  
**When you're using "type" as http you should choose method key**  
You can choose method from this list: 
https://www.iana.org/assignments/http-authschemes/http-authschemes.xhtml  
As represent below 
```yaml
security:
  - OAuth2:
    - read
    - write
components:
  securitySchemes:
    OAuth2:
      type: http
      scheme: basic
```