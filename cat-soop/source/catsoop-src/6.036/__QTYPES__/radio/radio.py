indiv = False

defaults = {'csq_soln':([],[]),
            'csq_check_function':lambda sub,soln: (sub.strip()==soln.strip()),
            'csq_npoints':1,
            'csq_pre':'',
            'csq_options':1,
            'csq_questionlabel':'',
            'csq_optionlabels':{},
            'csq_msg_function':lambda sub: (''),
            'csq_show_check':True}

def total_points(**kwargs):
    return 1

def handle_submission(submissions, **kwargs):
    return {'score': 1.0, 'msg': ''}

def render_html(last_log, **kwargs):
    info = dict(defaults)
    info.update(kwargs)
    out = '<tr>'
    out += '<td style="background-color:%s;padding:10px;">%s</td>' % (info['csq_shade'],info['csq_pre'])
    for i in range(info['csq_options']):
        out += '<td align="center" style="background-color:%s;padding:10px;"><input type="radio" name="%s_opts" value="%d" %s/></td>' % (info['csq_shade'],info['csq_name'],i,'checked' if last_log.get(info['csq_name'],"-1")==str(i) else '')
    out += '</tr>'
    out += '<input type="hidden" name="%s" id="%s" value="%s">' % (info['csq_name'],info['csq_name'],last_log.get(info['csq_name'],""))
    out += ('\n<script type="text/javascript">'
            '\ndocument.querySelectorAll("input[type=radio][name=%s_opts]").forEach(function(r){'
            '\n    r.addEventListener("click", function(){'
            '\n        document.getElementById("%s").value = this.value;'
            '\n    });'
            '\n});'
            '\n</script>') % (kwargs['csq_name'], kwargs['csq_name'])
    return out

def answer_display(**kwargs):
    return ""
