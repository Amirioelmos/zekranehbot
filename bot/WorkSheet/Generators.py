import jdatetime
import persian
import xlsxwriter

from bot.Utils.file_address import FileAddress
from bot.WorkSheet.Headers import WorkSheetHeaders
from bot.WorkSheet.Names import WorkSheetName


def _formatter(id):
    return persian.convert_en_numbers("1" + str(id).zfill(6))


def csv_file_for_all_unresolved_request_generator():
    requests = int(1)
    data = []
    for rq in requests:
        data.append([rq.id, rq.name, rq.father_name, rq.national_code,
                     rq.howze_code, rq.state, rq.edu_level, str(jdatetime.datetime.fromgregorian(datetime=rq.last_change))])

    workbook = xlsxwriter.Workbook(FileAddress.unresolved_request)
    worksheet = workbook.add_worksheet(WorkSheetName.unresolved_request)
    header = (_formatter(WorkSheetHeaders.id), WorkSheetHeaders.name, WorkSheetHeaders.father_name,
              WorkSheetHeaders.national_code,
              WorkSheetHeaders.howze_code, WorkSheetHeaders.state, WorkSheetHeaders.edu_level, WorkSheetHeaders.time)
    row_counter = 0
    worksheet.write_row(row_counter, 0, header)
    row_counter += 1
    for d in data:
        worksheet.write_row(row_counter, 0, d)
        row_counter += 1

    worksheet.autofilter('A1:G1')
    workbook.close()