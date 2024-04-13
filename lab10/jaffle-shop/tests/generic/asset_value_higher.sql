{% test is_value_higher(model, column_name, target_value=1) %}

with validation as (
    select
        {{ column_name }} as limit_field
    from {{ model }}
),

validation_errors as (
    select
        limit_field
    from validation
    where limit_field > {{target_value}}
)

select *
from validation_errors

{% endtest %}