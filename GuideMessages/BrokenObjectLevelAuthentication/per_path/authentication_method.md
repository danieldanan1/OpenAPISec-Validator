####Broken Object Level Authentication  
Please add authentication method as value of "BasicAuth" under components/securitySchemes as already defined   
As represent below 
```yaml
paths:
 /user:
  get:
   security:
   - BasicAuth : []
components:
 securitySchemes:
  BasicAuth:
   type: http
```