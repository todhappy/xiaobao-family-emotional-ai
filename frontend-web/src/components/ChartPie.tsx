import ReactECharts from "echarts-for-react"

export default function ChartPie({ data }: { data: { name: string, value: number }[] }) {
  const option = { series: [{ type: "pie", radius: "60%", data }] }
  return <ReactECharts option={option} style={{ height: 280 }} />
}