from models import Status

s = Status(status = "SALVO")
s.save()

s = Status(status = "PENDENTE")
s.save()

s = Status(status = "ANDAMENTO")
s.save()

s = Status(status = "CONCLUIDO")
s.save()

s = Status(status = "CANCELADO")
s.save()