####Broken Object Level Authentication  
**Please add authentication method as value of "type" key**  
You can choose method from this list: http, apiKey, openIdConnect, oauth2   
For more information: https://swagger.io/docs/specification/authentication/    
As represent below 
```yaml
paths:
 /user:
  get:
   security:
   - BasicAuth : []
   responses:
    default:
     description: Example
components:
 securitySchemes:
  BasicAuth:
   type: http
```