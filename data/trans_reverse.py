import csv  
from datetime import datetime 
import pytz
  
input_file = 'T_BTCUSDT-2017-2020-1d.csv'  # 输入文件路径（原程序的输出文件）  
output_file = 'reversed_output.csv'  # 输出文件路径  
  
# 由于我们不知道原数据的具体类型，这里假设：  
# - 第一列是日期，我们将尝试将其转换回时间戳  
# - 后面的列我们假设是数字（或可以转换为数字尝试），缺失的用0填充  
# - 如果原数据中有非数字列，这里可能会出错，但在这个简化示例中我们不考虑这种情况  
  
def date_to_timestamp(date_str):  
    # 尝试将日期字符串转换回时间戳  
    # 注意：这里的日期格式是'%Y%m%dT'，但原程序没有提供小时、分钟、秒和时区信息  
    # 因此，这里我们简单地假设日期是当天的00:00:00 UTC时间  
    # 如果日期格式或时区不同，请相应地调整  
    naive_datetime = datetime.strptime(date_str, '%Y%m%dT')  
    # 由于我们丢失了时区信息，这里我们假设是UTC时间（这可能不正确，但在这个示例中是必要的）  
    # 在实际应用中，你应该知道数据的正确时区  
    # defining the timezone
    tz = pytz.timezone('UTC')
    utc_datetime = tz.localize(naive_datetime)
    #utc_datetime = naive_datetime.replace(tzinfo=datetime.timezone.utc)  
    timestamp = int(utc_datetime.timestamp())  
    return timestamp  
  
# 打开输入和输出文件  
with open(input_file, mode='r', newline='', encoding='utf-8') as infile, open(output_file, mode='w', newline='', encoding='utf-8') as outfile:  
      
    reader = csv.reader(infile)  
    writer = csv.writer(outfile)  
      
    for row in reader:  
        # 假设第一列是日期，尝试转换回时间戳  
        try:  
            timestamp = date_to_timestamp(row[0])  
            # 将时间戳转换为浮点数（为了模拟原程序中的float(row[0])操作，尽管在这里可能不需要）  
            # 然后再转换为字符串，因为csv.writer处理的是字符串  
            timestamp_str = str(float(timestamp))  
        except ValueError as e:  
            # 如果转换失败（可能是因为日期格式不正确或其他原因），则使用原始字符串并打印警告  
            timestamp_str = row[0]  
            print(f"警告：无法将日期 {row[0]} 转换回时间戳，使用原始字符串。错误：{e}")  
          
        # 填充缺失的列到至少6列  
        # 假设后5列（除了第一列日期外）是数字或可以安全地转换为数字尝试，用0填充缺失的部分  
        # 如果原数据中有非数字列，这里可能会出错，需要更复杂的逻辑来处理  
        if len(row) < 6:  
            # 添加足够的0来填充到6列  
            row.extend(['0'] * (6 - len(row)))  
          
        # 由于我们不知道哪些列是原程序的“真实”数字列，这里我们简单地假设后5列都是  
        # 如果需要更精确的处理，需要额外的信息来确定哪些列是数字列  
        # 在这里，我们只是将后5列（除了已经处理过的第一列日期外）转换为字符串（如果它们不是的话）  
        # 并确保它们的长度与原始数据保持一致（尽管在这个逆程序中，我们实际上并不知道原始数据的完整长度）  
        # 因此，这里的处理可能并不完全准确，但提供了一个基本的框架  
        new_row = [timestamp_str] + [str(x) if isinstance(x, (int, float)) else x for x in row[1:6]] + ['0'] * 6
          
        # 写入输出文件  
        writer.writerow(new_row)  
  
print(f"处理完成，结果已保存到 {output_file}")