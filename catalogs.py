import enum

class ShippingStatus(enum.Enum):
    DELIVERED = 'Entregado'
    CANCELLED = 'Cancelado'
    IN_TRANSIT = 'En Tránsito'
    RETURNED = 'Retornado'
    DISPATCHED = 'Despachado'
    BOUGHT_IN_USA = 'Comprado en USA'


class Ship24MilestoneStatus(enum.Enum):
    PENDING = 'pending' # ShippingStatus.BOUGHT_IN_USA
    INFO_RECEIVED = 'info_received' # ShippingStatus.BOUGHT_IN_USA
    IN_TRANSIT = 'in_transit' # ShippingStatus.IN_TRANSIT
    OUT_FOR_DELIVERY = 'out_for_delivery' # ShippingStatus.DISPATCHED
    FAILED_ATTEMPT = 'failed_attempt' # ShippingStatus.RETURNED
    AVAILABLE_FOR_PICKUP = 'available_for_pickup' # ShippingStatus.RETURNED
    DELIVERED = 'delivered' # ShippingStatus.DELIVERED
    EXCEPTION = 'exception' # ShippingStatus.CANCELLED

# Mapping between Ship24MilestoneStatus and ShippingStatus
SHIP24_AND_OWN_STATUS_DICT = dict((
    (Ship24MilestoneStatus.PENDING.value, ShippingStatus.BOUGHT_IN_USA.value),
    (Ship24MilestoneStatus.INFO_RECEIVED.value, ShippingStatus.BOUGHT_IN_USA.value),
    (Ship24MilestoneStatus.IN_TRANSIT.value, ShippingStatus.IN_TRANSIT.value),
    (Ship24MilestoneStatus.OUT_FOR_DELIVERY.value, ShippingStatus.DISPATCHED.value),
    (Ship24MilestoneStatus.FAILED_ATTEMPT.value, ShippingStatus.RETURNED.value),
    (Ship24MilestoneStatus.AVAILABLE_FOR_PICKUP.value, ShippingStatus.RETURNED.value),
    (Ship24MilestoneStatus.DELIVERED.value, ShippingStatus.DELIVERED.value),
    (Ship24MilestoneStatus.EXCEPTION.value, ShippingStatus.CANCELLED.value)
))
