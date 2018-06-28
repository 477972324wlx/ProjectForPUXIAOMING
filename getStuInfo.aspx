<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="getStuInfo.aspx.cs" Inherits="WebApplication2.getStuInfo" %>

<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title></title>
</head>
<body>
    <form id="form1" runat="server">
        <p>
            <asp:Label ID="Label1" runat="server" Text="账号： "></asp:Label>
            <asp:TextBox ID="txt_id" runat="server" style="margin-bottom: 4px"></asp:TextBox>
        </p>
        <p>
            <asp:Label ID="Label2" runat="server" Text="密码： "></asp:Label>
            <asp:TextBox ID="txt_pwd" runat="server" OnTextChanged="TextBox1_TextChanged" ClientIDMode="AutoID" TextMode="Password"></asp:TextBox>
        </p>
        <p>
            <asp:Button ID="Button1" runat="server" OnClick="Button1_Click" Text="爬取个人信息" />
        </p>
        <p>
            <asp:Button ID="Button2" runat="server" Text="爬取教务新闻" OnClick="Button2_Click" />
        </p>
        <p>
            &nbsp;</p>
        <p>
            <asp:Label ID="Label3" runat="server" Text="贝叶斯gpa估分【注：贝叶斯限制了只能再已经选过的种类和学分数上进行预估】"></asp:Label>
        </p>
        <asp:Label ID="Label4" runat="server" Text="学科类别："></asp:Label>
        <asp:DropDownList ID="list_class" runat="server" Width="226px">
        </asp:DropDownList>
        <br />
        <asp:Label ID="Label5" runat="server" Text="学分数量："></asp:Label>
        <asp:DropDownList ID="list_score" runat="server" Width="226px">
        </asp:DropDownList>
        <p>
            <asp:Button ID="Button3" runat="server" Text="更新数据" Width="137px" OnClick="Button3_Click" />
            <asp:Button ID="Button4" runat="server" Text="开始估计" OnClick="Button4_Click" />
        </p>
    </form>
</body>
</html>
