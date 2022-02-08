from flask import url_for


def get_tree(base_req, dest_dict):
    dest_dict = {
        "id": base_req.id,
        "parent": base_req.parent_id,
        "title": base_req.title,
        "level": "R" if base_req.parent_id == 0 else 'SR',
        "priority": "کلیدی" if base_req.priority == 1 else "ضروری" if base_req.priority == 2 else "اختیاری",
        "req_type": "کارکردی" if base_req.req_type == 1 else 'غیرکارکردی',
        "changes": "سیمانی" if base_req.changes == 1 else 'بسامدی',
        "review": "رد" if base_req.review == 1 else "قبول" if base_req.review == 2 else "انتظار",
        "evaluation": "رد" if base_req.evaluation == 1 else "قبول" if base_req.evaluation == 2 else "انتظار" if base_req.evaluation == 3 else "ملاقات شده",
        "evaluation_method": "آنالیز" if base_req.evaluation == 1 else "شبیه سازی" if base_req.evaluation == 2 else "بازرسی" if base_req.evaluation == 3 else "تست سیستم" if base_req.evaluation == 4 else "تست کامپوننت",
        "quality_factor": q_fac(base_req.quality_factor),
        "description": base_req.description,
    }

    children = base_req.children

    if children:

        dest_dict['children'] = {}

        for child in children:
            dest_dict['children'] = get_tree(child, dest_dict)
            return dest_dict

    else:
        return dest_dict

    return dest_dict


def q_fac(q):
    if q == 1:
        return "AVAILABILITY"
    elif q == 2:
        return "FLEXBILITY"
    elif q == 3:
        return "INTEGRITY"
    elif q == 4:
        return "MAINTAINABILITY"
    elif q == 5:
        return "PORTABILITY"
    elif q == 6:
        return "RELIABILITY"
    elif q == 7:
        return "SAFETY"
    elif q == 8:
        return "SECURITY"
    elif q == 9:
        return "SUPPORTABILITY"
    elif q == 10:
        return "SUSTAINABILITY"
    else:
        return "USABILITY"


def get_dict(requirements, button):
    lists = []

    for req in requirements:

        d = dict({
            "tt_key": req.id,
            "tt_parent": req.parent_id,
            "title": req.title,
            "level": "R" if req.parent_id == 0 else 'SR',
            "priority": "کلیدی" if req.priority == 1 else "ضروری" if req.priority == 2 else "اختیاری",
            "req_type": "کارکردی" if req.req_type == 1 else 'غیرکارکردی',
            "changes": "سیمانی" if req.changes == 1 else 'بسامدی',
            "review": "رد" if req.review == 1 else "قبول" if req.review == 2 else "انتظار",
            "evaluation": "رد" if req.evaluation == 1 else "قبول" if req.evaluation == 2 else "انتظار" if req.evaluation == 3 else "ملاقات شده",
            "evaluation_method": "آنالیز" if req.evaluation == 1 else "شبیه سازی" if req.evaluation == 2 else "بازرسی" if req.evaluation == 3 else "تست سیستم" if req.evaluation == 4 else "تست کامپوننت",
            "quality_factor": q_fac(req.quality_factor),
            "description": req.description,
            "button": "<a href='{}' class='btn btn-sm  btn-info m-1' style='width:60px'>ویرایش</a> <a href='{}' "
                      "class='btn btn-sm  btn-danger m-1' style='width:60px'>حذف</a>".format(
                url_for('edit_req', req=req.id), url_for('requirement_remove', req=req.id))
        })
        if not button:
            d.pop('button', None)
        lists.append(d)

    return lists