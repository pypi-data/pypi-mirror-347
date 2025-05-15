"""
cself_tools 测试样例
"""
import os
import sys

sys.path.insert(0, os.path.abspath('.'))

from cself_tools import process_and_plot_mt_data


def main():
    """测试主函数"""
    print("cself_tools 测试样例")
    print("-------------------")

    # 测试使用不同的站点名称
    station_names = ["大山台"]

    for station_name in station_names:
        print(f"\n测试站点名称: {station_name}")

        # 仅作为示例，实际使用时需要有效的Oracle数据库连接
        # 由于缺少数据库连接，此测试将无法查询数据
        output_file = process_and_plot_mt_data(
            start_time="2021-01-01 00:00:00",
            end_time="2025-12-31 23:59:59",
            station_id="37024",
            point_id="E",
            frequencies=[22, 74],
            moving_avg_days=5,
            # 添加站点名称参数
            station_name=station_name,
            # 不主动初始化Oracle客户端，避免未安装oracle客户端的问题
            oracle_client_lib=None,
            # 测试自定义表名和列名（默认参数演示）
            # table_name="QZDATA.QZ_CP_372_90_AVG",
            # date_column="STARTDATE",
            # value_column="RYX",
            # stdv_column="RYXSTDV",
            # station_column="STATIONID",
            # point_column="POINTID",
            # freq_column="FREQUENCIES",
            show_plot=False)

        # 由于无法查询数据，期望结果为空字符串
        print(f"  测试完成，输出文件: {output_file}")

    # 返回测试结果代码（正常情况下均为空字符串）
    return 0


if __name__ == "__main__":
    sys.exit(main())
