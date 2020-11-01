

def user_content(user):
    ctx = {}
    ctx['narratives'] = user.narratives.all()
    ctx['series'] = user.series.all()
    ctx['highlights'] = ctx['narratives'][:5]
    return ctx
