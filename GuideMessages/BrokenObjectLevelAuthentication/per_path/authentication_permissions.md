####Broken Object Level Authentication  
**Please add to securitySchemes relevant permissions you defined in security label**  
As represent below 
```yaml
paths:
 /user:
  get:
   security:
   - BasicAuth : []
     - read
     - write
   responses:
    default:
     description: Example
components:
 securitySchemes:
  BasicAuth:
   type: http
   scheme: basic
   flows:
     authorizationCode:
       scopes:
         read: read objects in your account
         write: write objects to your account
```