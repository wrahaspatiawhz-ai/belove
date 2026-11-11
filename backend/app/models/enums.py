import enum


class UserRole(str, enum.Enum):
    admin = "admin"
    staff = "staff"


class OrderStatus(str, enum.Enum):
    pending = "pending"
    waiting_approval = "waiting_approval"
    revision = "revision"
    approved = "approved"
    waiting_payment = "waiting_payment"
    paid = "paid"
    in_production = "in_production"
    finishing = "finishing"
    packing = "packing"
    shipped = "shipped"
    completed = "completed"
    cancelled = "cancelled"


class InvoiceStatus(str, enum.Enum):
    draft = "draft"
    sent = "sent"
    approved = "approved"
    revision = "revision"
    paid = "paid"
    cancelled = "cancelled"


class PaymentStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    rejected = "rejected"


class StockMovementType(str, enum.Enum):
    in_ = "in"
    out = "out"
    adjustment = "adjustment"


class ProductCategory(str, enum.Enum):
    kaos = "kaos"
    sablon = "sablon"
    konveksi = "konveksi"


class OrderFileKind(str, enum.Enum):
    design = "design"
    mockup = "mockup"


class DtfStatus(str, enum.Enum):
    pending = "pending"
    checked = "checked"
    approved = "approved"
    rejected = "rejected"


class ProductionStepName(str, enum.Enum):
    stock_receipt = "stock_receipt"
    patch_cutting = "patch_cutting"
    printing = "printing"
    folding_accessories = "folding_accessories"
    finishing = "finishing"
    packing = "packing"


class ProductionStepStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"


class ConversationMode(str, enum.Enum):
    bot = "bot"
    human = "human"


class MessageDirection(str, enum.Enum):
    inbound = "inbound"
    outbound = "outbound"
