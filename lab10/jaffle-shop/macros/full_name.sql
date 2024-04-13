{% macro full_name_fun(f_name, l_name) %}
    ({{ f_name }} || {{ l_name }})
{% endmacro %}