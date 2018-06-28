using System;
using System.Collections.Generic;
using System.Data;
using System.Diagnostics;
using System.IO;
using Bayes;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace WebApplication2
{
    public partial class getStuInfo : System.Web.UI.Page
    {
        private static string CmdPath = @"C:\Windows\System32\cmd.exe";
        public static DataTable dataTable = new DataTable();
        static Dictionary<string, int> class_dict = new Dictionary<string, int>();
        static Dictionary<string, int> score_dict = new Dictionary<string, int>();
        protected void Page_Load(object sender, EventArgs e)
        {
            

        }

        protected void TextBox1_TextChanged(object sender, EventArgs e)
        {

        }

        protected void Button1_Click(object sender, EventArgs e)
        {
            string id = txt_id.Text;
            string pwd = txt_pwd.Text;
            string cmd = string.Format("python getStuInfo.py {0} {1}", id, pwd);
            RunCmd(cmd);
         
            RunCmd("start gpaChart.png");
            RunCmd("start timetable.gif");
        }

        public static void RunCmd(string cmd)
        {
            
            cmd = cmd.Trim().TrimEnd('&') + "&exit";//说明：不管命令是否成功均执行exit命令，否则当调用ReadToEnd()方法时，会处于假死状态
            using (Process p = new Process())
            {
                p.StartInfo.FileName = CmdPath;
                p.StartInfo.UseShellExecute = false;        //是否使用操作系统shell启动
                p.StartInfo.RedirectStandardInput = true;   //接受来自调用程序的输入信息
                p.StartInfo.RedirectStandardOutput = true;  //由调用程序获取输出信息
                p.StartInfo.RedirectStandardError = true;   //重定向标准错误输出
                p.StartInfo.CreateNoWindow = true;          //不显示程序窗口
                p.Start();//启动程序

                //向cmd窗口写入命令
                p.StandardInput.WriteLine("cd " + System.AppDomain.CurrentDomain.BaseDirectory);
                p.StandardInput.AutoFlush = true;
                p.StandardInput.WriteLine(cmd);
       

                p.StandardOutput.ReadToEnd();
                p.WaitForExit();//等待程序执行完退出进程
                p.Close();
            }
        }

        protected void Button3_Click(object sender, EventArgs e)
        {
            int cnt = 1;

            class_dict.Clear();
            score_dict.Clear();
            
            dataTable.Reset();
            list_class.Items.Clear();
            list_score.Items.Clear();
            dataTable.Columns.Add("gpa");
            dataTable.Columns.Add("class",typeof(double));
            dataTable.Columns.Add("score",typeof(double));
            DataTable dt = new DataTable();
            dt = OpenCSV(System.AppDomain.CurrentDomain.BaseDirectory+@"\gpa.csv");
            int len = dt.Rows.Count;
            for (int i = 1; i < len; ++i)
            {
                string _gpa = dt.Rows[i][4].ToString();
                string _class = dt.Rows[i][2].ToString();
                string _score = dt.Rows[i][3].ToString();
                if (!class_dict.ContainsKey(_class))
                {
                    class_dict.Add(_class, cnt++);
                    list_class.Items.Add(new ListItem(_class));
                }
                if (!score_dict.ContainsKey(_score))
                {
                    score_dict.Add(_score, 1);
                    list_score.Items.Add(new ListItem(_score));
                }

                dataTable.Rows.Add(_gpa, class_dict[_class], double.Parse(_score));

            }
        }

        protected void Button2_Click(object sender, EventArgs e)
        {
            string cmd = "python InfoNews.py";
            RunCmd(cmd);
            cmd = "start InfoUrl.csv";
            RunCmd(cmd);
        }
        public DataTable OpenCSV(string fileName)
        {
            DataTable dt = new DataTable();
            FileStream fs = new FileStream(fileName, System.IO.FileMode.Open, System.IO.FileAccess.Read);
            StreamReader sr = new StreamReader(fs, System.Text.Encoding.Default);
            //记录每次读取的一行记录
            string strLine = "";
            //记录每行记录中的各字段内容
            string[] aryLine;
            //标示列数
            int columnCount = 0;
            //标示是否是读取的第一行
            bool IsFirst = true;

            //逐行读取CSV中的数据
            while ((strLine = sr.ReadLine()) != null)
            {
                aryLine = strLine.Split(',');
                if (IsFirst == true)
                {
                    IsFirst = false;
                    columnCount = aryLine.Length;
                    //创建列
                    for (int i = 0; i < columnCount; i++)
                    {
                        DataColumn dc = new DataColumn(aryLine[i]);
                        dt.Columns.Add(dc);
                    }
                }
                else
                {
                    DataRow dr = dt.NewRow();
                    for (int j = 0; j < columnCount; j++)
                    {
                        dr[j] = aryLine[j];
                    }
                    dt.Rows.Add(dr);
                }
            }

            sr.Close();
            fs.Close();
            return dt;
        }

        protected void Button4_Click(object sender, EventArgs e)
        {
            string name = list_class.SelectedItem.Text;
            double score = double.Parse(list_score.SelectedItem.Text);
            int name_cnt = class_dict[name];

            Classifier classifier = new Classifier();
            classifier.TrainClassifier(dataTable);
            Response.Write(classifier.Classify(new double[] { name_cnt, score }));
        }
    }
}