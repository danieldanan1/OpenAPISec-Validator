# Quick Guide


**Path Definitions**

For given openapi spec and path you will get a response with relevant elements.  
The path parameter should be separate by '.'  

**Example 1**  [Full yaml](Rules/exampleYaml.yaml)
```yaml
   paths:
     /configuration:
       get:
         operationId: extensionConfiguration
         parameters:
           - in: header
             name: x-applecloudextension-session-id
             required: true
             schema:
               maxLength: 128
               minLength: 1
               type: string
           - in: header
             name: x-applecloudextension-retry-count
             required: false
             schema:
               format: uint32
               minimum: 1
               type: number
```
We have 4 permutations:
#### 1. Simple path
For example: *paths./configuration.get.operationId*  
Result: String/Dict
``` python
"extensionConfiguration"
```


#### 2. Path point to list
For example: paths./configuration.get.parameters is point to list of parameters  
Result: List  
```yaml
[{
  'in': 'header', 
  'name': 'x-applecloudextension-session-id', 
  'required': True, 
  'schema': 
           {
             'maxLength': 128, 
             'minLength': 1, 
             'type': 'string'
           }
},
{
  'in': 'header', 
  'name': 'x-applecloudextension-retry-count', 
  'required': False, 
  'schema': 
           {
             'format': 'uint32', 
             'minimum': 1, 
             'type': 'number'
           }
}]
```  
#### 3. Path contain a list 
For example: paths./configuration.get.parameters.schema.type is contain a list of parameters  
Result: List
```python
[
  "string",
  "number"
]
```
**Example 2**
```yaml
paths:
  /configuration:
    get:
      operationId: extensionConfiguration
      summary: Configuration Resource
  /intent/addMedia:
    post:
      operationId: addMediaIntentHandling
      summary: addMedia
  /intent/playMedia:
    post:
      operationId: playMediaIntentHandling
      summary: playMedia
```

#### 4. Path contain variable [placeholder]  
Path will use '#' symbol when you expect to get all parameters that exist under your path  
> Note: all elements that shouldn't match to your path pattern doesn't response as a result 

For example: paths.#var.post  
> Note: for this example 'get' isn't match to the path pattern   

Result: List 
```yaml
[{
  'operationId': 'addMediaIntentHandling',
  'summary': 'addMedia'
  },
	
  {
   'operationId': 'playMediaIntentHandling'
   'summary': 'playMedia'
}]
```

#### 5. Path contain variable    
Path will use '$' symbol when you expect to get a specific parameter that exist under your path  
> Note: when using '$' you should pay attention for his 'father' rule that contain '#' symbol in same name

For example: paths.$var.post.summary, when $var="/intent/addMedia"
Result: String/Dict [schema]
```python
"addMedia"
```

> **Note**: you can use all above examples as an combination to create a path  

## Rules
- The rule represent a logic unit use to analyze given openapi3 schema and return boolean value  
- [optional] Each rule can print a message in case of success/failure

#### Messages
each rule can contain the optional keys  
- **success_msg**: print when rule return true
- **fail_msg**: print when rule return false  

### Base Rule Definition

Pattern:
```
"path<string>,operator,[value<string>],[success_msg=<string>],[fail_msg=<string>]"
```

Base rule is an atomic unit should contain: 
- **path**
- **operator** 
- **value [depend operator]** 
- success_msg=message will raise when rule return true [optional] 
- fail_msg=message will raise when rule return false [optional]

#### Path: 
Mandatory
Should point to simple path [Example 1](#1.-simple-path)

#### Operator:
Mandatory
Defined actions to perform on given sub-scheme from below list:
- **exist**: return *true* if sub-scheme is exist  
- **not_exist**: return *true* if sub-scheme is not exist
- **lt**: return *true* if sub-scheme value is less than inserted number
- **gt**: return *true* if sub-scheme value is greater than inserted number
- **eq**: return *true* if sub-scheme value is equal to inserted number
- **any**: return *true* if value is exist in pre-defined list
- **contain**: return *true* if sub-scheme contain a given string value

#### Value  
Mandatory for this below operators:
- **lt**: int
- **gt**: int
- **eq**: int
- **any**: list of strings ["element1","element2"...]
- **contain**: string

#### Messages
Optional  
Structured as key and value which use delimiter '='
- success_msg
- fail_msg
`

### Condition Rule
Pattern:
```yaml
{
  "condition": "<rule>"
  "true": "<rule>"
  "false": "<rule>"
}
```
- **Condition**: mandatory, condition contain rule and when defined rule is true,
the engine will run true key else the false key
- **true**: optional, in case the condition return true this part will run and the result of this section will by the result of the all rule
- **false**: optional, in case the condition return false this part will run and the result of this section will by the result of the all rule
> **Note**:   
> - If true key is not defined and the condition value is true, rule will return true  
> - If false key is not defined and the condition value is false, rule will return true


### And Rule
Pattern:
```yaml
{
  "and": ["<rule>"]
}
```
- **And**: mandatory, expect to list of rules and if all rules return true the all rule return true


### Or Rule
Pattern:
```yaml
{
  "or": ["<rule>"]
}
```
- **Or**: mandatory, expect to list of rules and if at least one rule return true the all rule return true

### All Rule
Pattern:
```yaml
{
  "all": "path_of_array",
  "rule": "<rule>"
}
```
- **All**: mandatory, expect to path point to a list of sub-scheme
- **Rule**: mandatory, if the rule return true from each element, then 'all' return true. 

###Any Rule
Pattern:
```yaml
{
  "any": "path_of_array",
  "rule": "<rule>"
}
```
- **Any**: mandatory, expect to path point to a list of sub-scheme
- **Rule**: mandatory, if the rule return true from at least one element, then 'any' return true. 

