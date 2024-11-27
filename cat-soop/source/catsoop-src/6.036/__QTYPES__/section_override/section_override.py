import logging
import datetime

LOGGER = logging.getLogger("cs")

# indiv = False

defaults = {'csq_soln': "",
            'csq_check_function':lambda sub,soln: (sub.strip()==soln.strip()),
            'csq_npoints':1,
            'csq_pre':'',
            'csq_msg_function':lambda sub, soln: '',
            'csq_show_check':False,
            'csq_override_valid_time_delta': datetime.timedelta(days=5),
}

def total_points(**kwargs):
    return 1

def delete_section_override(username):
    LOGGER.info("[section_override] deleting section override for username=%s" % (username))
    db_name = "section_override"
    data = csm_cslog.most_recent(db_name, [], username)
    if not data or 'expiration' not in data:
        LOGGER.info("[section_override] no existing override for username=%s!" % (username))
        return False
    current_user = cs_user_info['username']
    data = {'deleted_by': current_user,
            'username': username,
    }
    csm_cslog.update_log(db_name, [], username, data)
    return True

def add_section_override(username, secnum, expiration):
    LOGGER.info("[section_override] adding section override for username=%s, secnum=%s" % (username, secnum))
    db_name = "section_override"
    current_user = cs_user_info['username']
    data = {'added_by': current_user,
            'username': username,
            'secnum': int(secnum),
            'expiration' : expiration,
    }
    csm_cslog.update_log(db_name, [], username, data)

def handle_submission(submissions, **kwargs):
    LOGGER.error("[section_override] submissions=%s" % str(submissions))
    info = dict(defaults)
    info.update(kwargs)
    course = info['csq_course']
    context = globals()
    course_users = csm_util.all_users_info(context, course)	# { username: user_info }

    username = submissions['__q000000_0000']
    secnum = submissions['__q000000_0001']
    dt = datetime.datetime.now()
    vtd = info['csq_override_valid_time_delta']
    expiration = dt + vtd

    sections = info['csq_sections']
    msg = 'username=%s, secnum=%s<br/>' % (username, secnum)
    #msg += 'Delta time = ' + str(vtd)
    ok = False
    if not username in course_users:
        msg += '<br/><font color="red" size="4">ERROR!  Username "%s" is unknown (not in course users)</font>' % username
    else:
        uinfo = course_users[username]
        allsections = sections + ["Staff"]
        usecname = allsections[uinfo.get('section')]
        if secnum=="delete":
            dok = delete_section_override(username)
            if dok:
                msg += '<br/><font color="green" size="4">Ok!  Username "%s" known, deleting section override</font>' % username
            else:
                msg += '<br/><font color="orange" size="4">Username "%s" known, but no existing override to be deleted</font>' % username
            ok = False
        else:
            args = (username, secnum, sections[int(secnum)])
            msg += '<br/><font color="green" size="4">Ok!  Username "%s" known, section override added for %s: %s</font>' % args
            msg += "<br/>"
            msg += '<br/>This override is valid until %s' % expiration
            ok = True

        msg += '<br/> User "%s" is normally in section %s: %s' % (username, uinfo.get('section'), usecname)
        if "full_name" in uinfo:
            msg += "<br/> User full name: %s" % uinfo['full_name']
        if "subject" in uinfo:
            msg += "<br/> User subject: %s" % uinfo['subject']
        if "registration_status" in uinfo:
            status = uinfo['registration_status']
            if status == 'Listener':
                msg += "<br/><b>Warning!"
            else:
                msg += "<br/>"
            msg += " User registration status: %s" % uinfo['registration_status']
            if status == 'Listener':
                msg += "</b>"

    msg += "<br/><font color='gray' size=1>submission=%s</font>" % str(submissions)

    if ok:
        add_section_override(username, secnum, expiration)

    return {'score': 1.0, 'msg': msg}

def render_html(last_log, **kwargs):
    LOGGER.error("[section_override] last_log=%s, kwargs=%s" % (last_log, len(kwargs)))
    info = dict(defaults)
    info.update(kwargs)
    cname = info['csq_name']
    cnames = ["__%s_%04d" % (cname, x) for x in range(2)]

    sections = info['csq_sections']
    sections_table = dict(zip(range(0, len(sections)+2), sections))
    sections_table['delete'] = "<font color='red'>Delete</font>"
    
    LOGGER.info("[section_override] cname=%s" % cname)
    out = '<table border=1>'
    out += '<tr><td>username</td><td>new (temporary) section</td></tr>'
    out += '<tr>'
    out += '<td><input type="text" name="%s" value="%s" id="%s"/></td>' % (cnames[0],
                                                                           last_log.get(cnames[0], ""),
                                                                           cnames[0])
    out += '<td><select type="text" name="%s" value="%s" id="%s">' % (cnames[1],
                                                                       last_log.get(cnames[1], ""),
                                                                       cnames[1])
    for secnum, secname in sections_table.items():
        out += '<option value="%s">%s</option>' % (secnum, secname)
    out += "</select>"
    out += "</td>"
    out += '</tr>'
    out += "</table>"
    return out

def answer_display(**kwargs):
    return ""
