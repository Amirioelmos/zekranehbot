class Command:
    del_admin = "/del_admin"
    add_admin = "/add_admin"
    myid = "/myid"
    help = "/help"
    start = "/start"
    menu = "/menu"


class ButtonAction:
    default = 0


class Patterns:
    bale_id = "^\d{3,}$"
    back_to_replied = "^بازگشت به پیام‌های پاسخ داده شده$"
    return_to_main_menu = "^بازگشت به منوی اصلی$"
    phone_number_pattern = "^(\+98|0)?9\d{9}$"  # "(^09[0-9]{9}$)|(^9[0-9]{9}$)"
    fullname = "[\D]{7,130}"  # "^[\sآابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی‬ٌ ‬ًّ ‬َ ‬ِ ‬ُ ‬]{5,30}$"  # "[\u0600-\u06FF\s]{5,30}"


class MimeType:
    image = "image/jpeg"
    csv = "text/csv"
    xlsx = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


class BotMessage:
    choose_one_option = "یکی از موارد زیر را *انتخاب* نمایید:"
    choose_page_book_mark = "یکی از *صفحات منتخب* را انتخاب کنید، یا"
    removed_from_book_mark = "صفحه *{}* به صفحات منتخب حذف شد."
    added_to_book_mark = "صفحه *{}* به صفحات منتخب افزوده شد."
    wrong_input_page = "ورودی صحیح *نیست* - شماره صفحه باید بین *۱* الی *۶۰۴* باشد"
    choose_page_number = "*شماره صفحه* مورد نظر برای *مطالعه* را وارد نمایید:"
    continue_msg = "در ادامه قصد انجام چه کاری دارید:"
    wrong_input = "ورودی صحیح *نیست*"
    aye_text = "سوره مبارکه: *{}،* آیه *{}*\n*متن آیه* :\n{}"
    tarjome_text = "*متن ترجمه* :\n{}"
    tafsir_text = "*متن تفسیر* :\n{}"
    choose_aye_number = "شماره آیه مورد نظر را وارد نمایید:\nسوره مبارکه *{}* دارای *{}* آیه می باشد."
    choose_soore = "سوره مورد نظر را انتخاب نمایید:"

    add_admin_id = "لطفا آی دی ادمین جدید را وارد کنید:"
    not_found_admin = "آی دی وارد شده در لیست کاربران بازو یافت نشد."
    no_admin_right = "*شما دسترسی ادمین روت ندارید!*"
    del_admin = "ادمین مورد نظر حذف شد"
    add_admin = "ادمین جدید با موفقیت اضافه شد.\n" \
                "نام: *{}*  نام کاربری: *{}*"
    choose_admin = "ادمین مورد نظر را انتخاب کنید:"
    guide_text = "این راهنما است."
    enter_your_pass = "رمز عبور خود را وارد کنید"
    message_sent = "پیام شما ارسال شد"
    choose_from_menu = "یکی از موارد زیر را انتخاب کنید"
    greeting = "سلام\n به بازوی *ذکرانه* خوش آمدید"


class ConversationData:
    username = "username"
    name = "name"


class Regex:
    bank_calculate = "^محاسبه‌یار$"
    bank_locator = "^ملّی‌یاب$"
    number_only = '^([0-9]+|[۰-۹]+)$'
    numbers = '([0-9]+|[۰-۹]+)'
    search_by_id = "((A|B)-{}-{})|{}".format(numbers, numbers, number_only)
    percent_regex = "(^[1-9][0-9]?$|^100$)|(^[۱-۹][۰-۹]?$|^۱۰۰$)"
    persian_regex = "[ء|\s|آ-ی]+"
    book_mark = "^افزودن به شعب منتخب:*"


class ButtonMessage:
    read_page = "👁 مطالعه صفحه {}"
    remove_from_book_mark = "❌ حذف از صفحات منتخب"
    back_to_read = "⤴️ بازگشت به مطالعه صفحه {}"
    add_to_book_mark = "📎 افزودن به صفحات منتخب"
    next_page = "⬅️ صفحه بعد"
    before_page = "➡️ صفحه قبل"
    read = "📖 مطالعه صفحات قرآن"
    tafsir = "تفسیر آیات قرآن"
    show_more = "نمایش بیشتر"
    tarjome = "ترجمه آیات قرآن"
    return_to_back_step = "بازگشت به مرحله‌ی قبل"
    report = "گزارش"
    yes = "بله"
    return_to_main_menu = "🔄 بازگشت به منوی اصلی"
    guide = "راهنما"


class SendingAttempt:
    first = 1


class Step:
    show_guide = "show_guide"
    showing_menu = "showing_menu"
    conversation_starter = "conversation_starter"


class LogMessage:
    failed_report_sending = "failed report sending"
    successful_report_sending = "successful report sending"
    failed_report_upload = "failure report uploading"
    successful_report_upload = "successful report uploading"
    user_register = "successful user register"
    successful_sending = "successful sending of message:"
    failed_sending = "failed sending of message:"
    successful_step_message_sending = "successful step message sending"
    failed_step_message_sending = "failure step message sending"


class UserData:
    path = "path"
    number = "number"
    record_changes_num = "record_changes_num"
    url = "url"
    file_id = "file_id"
    succedent_message = "succedent_message"
    latitude = "latitude"
    longitude = "longitude"
    bot = "bot"
    send_message = "send_message"
    logger = "logger"
    session = "session"
    message_type = "message_type"
    message_id = "message_id"
    sending_set_time = "sending_set_time"
    base_message = "base_message"
    db_msg = "db_msg"
    random_id = "random_id"
    sending_attempt = "sending_attempt"
    kwargs = "kwargs"
    user_id = "user_id"
    user_peer = "user_peer"
    step_name = "step_name"
    message = "message"
    attempt = "attempt"
    report_attempt = "report_attempt"
    doc_message = "doc_message"
    file_url = "file_url"
    thumb="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"
