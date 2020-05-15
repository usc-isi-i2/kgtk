The current mapping between OWL and OpenAPI specification (OAS) supported by OBA can be seen below.

!!! warning
    We are currently working on improving the mapping with complex axiomatization of domains and ranges and other property annotations (minimum and maximum cardinality, etc.)

**Namespaces** used in this document:

  - owl: [http://www.w3.org/2002/07/owl#](http://www.w3.org/2002/07/owl#)
  - rdfs: [http://www.w3.org/2000/01/rdf-schema#](http://www.w3.org/2000/01/rdf-schema#)
  - skos: [http://www.w3.org/2004/02/skos/core#](http://www.w3.org/2004/02/skos/core#)
  - prov: [http://www.w3.org/ns/prov#](http://www.w3.org/ns/prov#)

## owl:Class

Each class in the ontology is associated with two paths for the GET operation, one path for POST, PUT and DELETE operations; and a schema. For example, consider the class "Plan" from [http://purl.org/net/p-plan](http://purl.org/net/p-plan). The following GET paths would be generated: 

```yaml
/plans:
  get:
        description: Gets a list of all instances of Plan (more information in http://purl.org/net/p-plan#Plan)
        parameters:
        {...} #omitted for simplicity
        responses:
        200:
          content:
            application/json:
              schema:
                items:
                  $ref: '#/components/schemas/Plan'
                type: array
          description: Successful response - returns an array with the instances of Plan.
          headers:
            link:
              description: Information about pagination
              schema:
                type: string
      summary: List all instances of Plan
```

```yaml
/plans/{id}:
    get:
      description: Gets the details of a given Plan (more information in http://purl.org/net/p-plan#Plan)
      parameters:
      {...} #omitted for simplicity, the response is similar to the one above
```
And the following Schema would be generated:

```yaml
Plan:
      description: A p-plan:Plan is a specific type of prov:Plan. It is composed of smaller steps that use and produce Variables.
      properties:
        wasGeneratedBy:
        {...} #omitted other properties for simplicity.
```

### rdfs:subClassOf

Subclasses inherit all properties from their respective superclasses. The OpenAPI specification has the `allOf` clause to indicate this behavior. However, this was not supported by any existing generators until very recently, and therefore OBA will iterate through all superclasses to add the appropriate properties for a given schema.

## owl:ObjectProperty

Each object property is added to its corresponding schema definition that uses it as domain. For example, in the P-Plan ontology, `Plan` has a property `isSubPlanofPlan` which has domain `Plan`. This would be represented as follows in the OpenAPI specification:

```yaml
 Plan:
      description: A p-plan:Plan is a specific type of prov:Plan. It is composed of smaller steps that use and produce Variables.
      properties:
        isSubPlanOfPlan:
          description: A p-plan:Plan may be a subplan of another bigger p-plan:Plan. p-plan:isSubPlanOfPlan is used to state the link among the two different plans. 
          items:
            $ref: '#/components/schemas/Plan'
          nullable: true
          type: array
```

## owl:DataTypeProperty

Similar mapping to an objec property, except that no schemas will be used as reference under the `items` field. For example, consider a `dateCreated` property that indicates when an item is created:

```yaml
dateCreated:
          description: Creation date of the item
          items:
            type: string
          nullable: true
          type: array
```

### rdfs:domain and rdfs:range

For each object and datatype property, OBA will analyze their `rdfs:domain` and `rdfs:range` to assign the property in the right schema (using `rdfs:domain`) and use the appropriate reference or datatype (by inspecting `rdfs:range`). At the moment, cardinality constraints are not taken into account in this mapping.


## Other important considerations

All properties are `nullable` (i.e., optional) and are returned as a list. This is because from the development perspective, it is easier to deal with lists (even if they have one element) than having to distinguish whether the object returned is a list or not.

Complex unions and intersections are considered of type `object` instead of a particular schema.

## Class and property documentation
OBA uses `rdfs:comment`, `skos:definition` and `prov:definition` annotations in the ontology for creating definitions of the classes and properties in OBA. An example can be seen below: 

Example:
```yaml
Plan:
      description: A p-plan:Plan is a specific type of prov:Plan. It is composed of smaller steps that use and produce Variables.
      properties:
        isSubPlanOfPlan:
          description: A p-plan:Plan may be a subplan of another bigger p-plan:Plan. p-plan:isSubPlanOfPlan is used to state the link among the two different plans. Note that if p1 is a p-plan:subPlan of p2, p1will not necessarily be a step of p2. A multistep will represent p1 in p2, and link to p1 with the p-plan.hasStepDecomposition relationship.
        {...} #Rest of the schema ommited for brevity
```


