from django.template.defaulttags import register


@register.filter
def visible(description):
    if len(description) < 500:
        return description
    else:
        buf = description[:500]
        if buf[-1] != ".":
            remain = description.replace(buf, " ")
            # Сделать проверку если нет точки в предложении
            ind = remain.index(".")
            try:
                while remain[ind] == ".":
                    ind += 1
                buf += remain[:ind]
            except IndexError:
                buf += remain
        return buf


@register.filter
def hidden(description):
    if len(description) < 500:
        return False
    else:
        buf = description[:500]
        if buf[-1] != ".":
            remain = description.replace(buf, " ")
            ind = remain.index(".")
            try:
                while remain[ind] == ".":
                    ind += 1
                return remain[ind:]
            except IndexError:
                return False
