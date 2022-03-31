###Broken Object Level Authentication  
**Please add authentication lable under global security**  
As represent below add label and scope permissions  
> Note: Please make sure you also implement it in securityScheme
```yaml
security:
  - OAuth2:
    - read
    - write
```