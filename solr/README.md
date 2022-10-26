# Search engine for question answering
## Solr

Most concepts are briefly described in
[Official Solr Tutorials](https://solr.apache.org/guide/solr/latest/getting-started/solr-tutorial.html)
being enough for understanding queries and indexing concepts.

Within [Apache Solr Reference Guide](https://solr.apache.org/guide/solr/latest/)
you can find more detailed description of many Solr concepts, among which
the most relevant include:
* [Solr in Docker](https://solr.apache.org/guide/solr/latest/deployment-guide/solr-in-docker.html)
* [Solr Configuration Files](https://solr.apache.org/guide/solr/latest/configuration-guide/configuration-files.html)
* [Configsets](https://solr.apache.org/guide/solr/latest/configuration-guide/config-sets.html)
* [Fields](https://solr.apache.org/guide/solr/latest/indexing-guide/fields.html)
* [Schema Elements](https://solr.apache.org/guide/solr/latest/indexing-guide/schema-elements.html)

## Setup using docker-compose.yml
You can manage solr by `docker-compose`.
After using

```docker-compose up [-d]```

you can access `solr` it via `localhost:8983`.
Both by UI in browser and by plain HTTP with `curl`.

It is prepared using official
[Solr in Docker](https://solr.apache.org/guide/solr/latest/deployment-guide/solr-in-docker.html).
To enable Polish, we have to set `SOLR_MODULES=analysis-extras`,
as described in [Polish-related section](https://solr.apache.org/guide/solr/latest/indexing-guide/language-analysis.html#polish).

We have extended `_default` Solr configset with field type for Polish text
and Q&A fields using this type.

```xml
    <dynamicField name="*_txt_pl" type="text_pl"  indexed="true"  stored="true"/>
    <fieldType name="text_pl" class="solr.TextField" positionIncrementGap="100">
      <analyzer>
        <tokenizer name="standard"/>
        <filter name="morfologik" dictionary="morfologik/stemming/polish/polish.dict"/>
        <filter name="lowercase"/>
      </analyzer>
    </fieldType>
    <field name="Q" type="text_pl" indexed="true" stored="true" required="true" multiValued="false"/>
    <field name="A" type="text_pl" indexed="true" stored="true" required="true" multiValued="false"/>
```
Dialogs core is created during startup, using this extended configset as specified in

`command: solr-create -c dialogs -d /var/solr/configsets/dialogs`

To index documents you can follow guide about
[JSON Formatted Index Updates](https://solr.apache.org/guide/solr/latest/indexing-guide/indexing-with-update-handlers.html#json-formatted-index-updates).
You can do it using any tool which alllows you to use HTTP,
including `curl` and Python `requests`.

To index `dialogs.json` you can simply use

```bash
curl 'http://localhost:8983/solr/dialogs/update?commit=true' --data-binary @data/dialogs.json -H 'Content-type:application/json'
```

## Queries

After Solr setup and indexing questions and answers,
you are ready to prepare and use queries.
For prototyping the best way is using UI at http://localhost:8983/solr/#/dialogs/query.