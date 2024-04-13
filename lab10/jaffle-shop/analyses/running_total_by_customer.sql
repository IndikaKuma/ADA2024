with customers as (

    select * from {{ ref('stg_customers') }}

),

orders as (

    select * from {{ ref('stg_orders') }}

),

payments as (

    select * from {{ ref('stg_payments') }}

),

customers_orders as (

    select customers.customer_id,
           orders.order_id

    from customers
    inner join orders on customers.customer_id = orders.customer_id
),

orders_payments as (

    select orders.order_id,
            payments.amount
    from orders
    inner join payments on orders.order_id = orders.order_id
),

final as (

    select
        customers_orders.customer_id,
        sum(orders_payments.amount)

    from customers_orders

    inner join orders_payments
        on customers_orders.order_id = orders_payments.order_id

    group by customers_orders.customer_id
)

select * from final
