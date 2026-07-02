{% macro generate_schema_name(custom_schema_name, node) -%}
    {# Usa staging / intermediate / marts sin prefijo public_ #}
    {%- if custom_schema_name is none -%}
        {{ target.schema }}
    {%- else -%}
        {{ custom_schema_name | trim }}
    {%- endif -%}
{%- endmacro %}
