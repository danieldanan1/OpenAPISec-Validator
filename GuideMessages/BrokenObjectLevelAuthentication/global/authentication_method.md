####Broken Object Level Authentication  
Please add authentication method as value of "OAuth2" under components/securitySchemes as already defined   
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