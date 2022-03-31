###Broken Object Level Authentication  
**Please add security lable for each method in your path**  
As represent below add label and scope permissions  
```yaml
paths:
 /user:
  get:
   security:
   - BasicAuth : []
   
```