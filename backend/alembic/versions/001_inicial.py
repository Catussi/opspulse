"""Esquema inicial de OpsPulse."""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "001_inicial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "pedidos",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("codigo_pedido", sa.String(length=64), nullable=False),
        sa.Column("producto", sa.String(length=200), nullable=False),
        sa.Column("cantidad", sa.Integer(), nullable=False),
        sa.Column("precio_unitario", sa.Float(), nullable=False),
        sa.Column("region", sa.String(length=100), nullable=False),
        sa.Column("fecha_pedido", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "creado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("codigo_pedido"),
    )
    op.create_index("ix_pedidos_codigo_pedido", "pedidos", ["codigo_pedido"])
    op.create_index("ix_pedidos_producto", "pedidos", ["producto"])

    op.create_table(
        "eventos_ingesta",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("fuente", sa.String(length=255), nullable=False),
        sa.Column("tipo_fuente", sa.String(length=32), nullable=False),
        sa.Column("estado", sa.String(length=32), nullable=False),
        sa.Column("filas_exitosas", sa.Integer(), nullable=False),
        sa.Column("filas_rechazadas", sa.Integer(), nullable=False),
        sa.Column("mensaje_error", sa.Text(), nullable=True),
        sa.Column(
            "creado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "actualizado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "reglas_automatizacion",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nombre", sa.String(length=150), nullable=False),
        sa.Column("tipo_condicion", sa.String(length=64), nullable=False),
        sa.Column("umbral", sa.Float(), nullable=False),
        sa.Column("url_webhook", sa.String(length=500), nullable=True),
        sa.Column("activa", sa.Boolean(), nullable=False),
        sa.Column("descripcion", sa.Text(), nullable=True),
        sa.Column(
            "creado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("reglas_automatizacion")
    op.drop_table("eventos_ingesta")
    op.drop_index("ix_pedidos_producto", table_name="pedidos")
    op.drop_index("ix_pedidos_codigo_pedido", table_name="pedidos")
    op.drop_table("pedidos")
