using System;
using System.Data;
using System.Drawing;
using System.Drawing.Printing;
using System.Windows.Forms;
using System.Windows.Forms.VisualStyles;

namespace WindowsFormsApp1
{
    public partial class Form1 : Form
    {
        Timer timer;
        public static int tk = 0;

        public static int[,] pole;
        public static Button[,] button;
        public static Button buttonFlag;
        public static Button buttonMain;
        public static TextBox textBoxTime;
        public static TextBox textBoxMine;
        public static ComboBox comboBox;
        public static int col = 9;//количество столбцов
        public static int row = 9;//количество строк
        public static int n = 10; //кол-во мин
        public static int save_kl; //безопасные клетки
        public static int index = 0;
        
        public static void Shuffle(int[] arr)
        {
            // создаем экземпляр класса Random для генерирования случайных чисел
            Random rand = new Random();
            for (int i = arr.Length - 1; i >= 1; i--)
            {
                int j = rand.Next(i + 1);

                int tmp = arr[j];
                arr[j] = arr[i];
                arr[i] = tmp;
            }
        }

        public static int Randomly(int a)
        {
            Random rand = new Random();
            return rand.Next(a);
        }
        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            timer = new Timer();
            timer.Tick += timer_Tick;
            tk = 0;
            
            //Размер формы = размеру экрана
            this.WindowState = FormWindowState.Maximized;
            this.BackColor = Color.Azure;

            //Начально количество столбцов и строк и координыт ценрта
            int x0 = this.Width / 2;
            int y0 = this.Height / 2;
            int h_w = 50;
            int height = row * h_w;
            int width = col * h_w;

            save_kl = row * col - n;

//            //создание таблицы
//            DataGridView dataGridView = new DataGridView();
//            dataGridView.ColumnHeadersVisible = false;
//            dataGridView.RowHeadersVisible = false;
//            dataGridView.AllowUserToAddRows = false;
//            dataGridView.AllowUserToResizeColumns = false;
//            dataGridView.AllowUserToResizeRows = false;

            Random rand = new Random();
            int[] randi = new int[n];
            int[] randj = new int[n];

            if (index == 0)
            {
                for (int i = 0; i <  n; i++)
                {
                    randi[i] = i;
                }
            
                Shuffle(randi);
                
                for (int j = 0; j < n; j++)
                {
                    randj[j] = rand.Next(j);
                }
            }
            else
            {
                for (int i = 0; i < n; i++)
                {
                    if (i >= row)
                        randi[i] = row - 1 - Randomly(rand.Next(row - 1));
                    else
                        randi[i] = i;
                }

                Shuffle(randi);

                for (int j = 0; j < n; j++)
                {
                    if (j >= col)
                        randj[j] = col - 1 - Randomly(rand.Next(col - 1));
                    else
                        randj[j] = j;
                }
            }

            //окантовка поля
            RichTextBox richTextBox = new RichTextBox();
            richTextBox.ReadOnly = true;
            richTextBox.Height = row * h_w + 20;
            richTextBox.Width= col * h_w + 20;
            richTextBox.Location = new Point(x0 - richTextBox.Width / 2,y0 - richTextBox.Height / 2);
            richTextBox.BackColor = Color.SlateGray;
            Controls.Add(richTextBox);
            
            //окантовка заголовка
            RichTextBox richTextBox2 = new RichTextBox();
            richTextBox2.ReadOnly = true;
            richTextBox2.Height = 70;
            richTextBox2.Width = richTextBox.Width;
            richTextBox2.BackColor = Color.SlateGray;
            richTextBox2.Location = new Point(x0 - richTextBox.Width / 2, y0 - richTextBox.Height / 2 - 70);
            Controls.Add(richTextBox2);
            
            //кнопка перезапуска
            buttonMain = new Button();
            buttonMain.Height = 46;
            buttonMain.Width = 46;
            buttonMain.Location = new Point(x0 - buttonMain.Width / 2, y0 - richTextBox.Height / 2 - richTextBox2.Height / 2 - buttonMain.Height / 2);
            buttonMain.Name = "buttonMain";
            buttonMain.Click += ButtonMainOnclick;
            buttonMain.Image = Image.FromFile("C:\\Users\\fesevu\\Desktop\\Лабораторные работы\\Игра\\smile.jpg");
            Controls.Add(buttonMain);
            buttonMain.BringToFront();
            
            //текстовое поле с количеством мин
            textBoxMine = new TextBox();
            textBoxMine.Multiline = true;
            textBoxMine.ReadOnly = true;
            textBoxMine.Font = new Font("Arial", 28, FontStyle.Bold);
            textBoxMine.TextAlign = HorizontalAlignment.Center;
            textBoxMine.Text = "\n \n \n" + n.ToString();
            textBoxMine.Height = buttonMain.Height;
            textBoxMine.Location = new Point(richTextBox.Location.X + 60,
                y0 - richTextBox.Height / 2 - richTextBox2.Height / 2 - textBoxMine.Height / 2);
            textBoxMine.Width = buttonMain.Location.X - textBoxMine.Location.X - 20;
            Controls.Add(textBoxMine);
            textBoxMine.BringToFront();
            
            //изображение мины
            Button buttonMine = new Button();
            buttonMine.BackColor = richTextBox2.BackColor;
            buttonMine.FlatAppearance.BorderColor = richTextBox2.BackColor;
            buttonMine.FlatAppearance.BorderSize = 0;
            buttonMine.Enabled = false;
            buttonMine.ForeColor = richTextBox2.BackColor;
            buttonMine.Image = Image.FromFile("C:\\Users\\fesevu\\Desktop\\Лабораторные работы\\Игра\\мина.jpg");
            buttonMine.Height = textBoxMine.Height;
            buttonMine.Width = buttonMain.Width;
            buttonMine.Location = new Point(textBoxMine.Location.X - 53, textBoxMine.Location.Y);
            Controls.Add(buttonMine);
            buttonMine.BringToFront();
            
            
            //текстовое поле с таймером
            textBoxTime= new TextBox();
            textBoxTime.Multiline = true;
            textBoxTime.ReadOnly = true;
            textBoxTime.Font = new Font("Arial", 28, FontStyle.Bold);
            textBoxTime.TextAlign = HorizontalAlignment.Center;
            textBoxTime.Text = "0";
            textBoxTime.Height = buttonMain.Height;
            textBoxTime.Location = new Point(buttonMain.Location.X + buttonMain.Width + 20,
                y0 - richTextBox.Height / 2 - richTextBox2.Height / 2 - textBoxTime.Height / 2);
            textBoxTime.Width = richTextBox2.Location.X + richTextBox2.Width  - 60 - textBoxTime.Location.X ;
            Controls.Add(textBoxTime);
            textBoxTime.BringToFront();
            
            //изображение часов
            Button buttonTime = new Button();
            buttonTime.BackColor = richTextBox2.BackColor;
            buttonTime.FlatAppearance.BorderColor = richTextBox2.BackColor;
            buttonTime.FlatAppearance.BorderSize = 0;
            buttonTime.Enabled = false;
            buttonTime.ForeColor = richTextBox2.BackColor;
            buttonTime.Image = Image.FromFile("C:\\Users\\fesevu\\Desktop\\Лабораторные работы\\Игра\\watch.jpg");
            buttonTime.Height = textBoxTime.Height;
            buttonTime.Width = buttonMain.Width;
            buttonTime.Location = new Point(textBoxTime.Location.X + textBoxMine.Width + 7, textBoxTime.Location.Y);
            Controls.Add(buttonTime);
            buttonTime.BringToFront();
            
            //отмечаем мины
            buttonFlag = new Button();
            buttonFlag.Width = 50;
            buttonFlag.Height = 52;
            buttonFlag.Text = "";
            buttonFlag.Location = new Point(richTextBox.Location.X, richTextBox.Location.Y + richTextBox.Height);
            buttonFlag.Image = Image.FromFile("C:\\Users\\fesevu\\Desktop\\Лабораторные работы\\Игра\\point.jpg");
            buttonFlag.Click += ButtonFlagOnclick;
            Controls.Add(buttonFlag);
            
            //сложность
            comboBox = new ComboBox();
            comboBox.Height = buttonFlag.Height;
            comboBox.Width = 150;
            comboBox.Location = new Point(buttonFlag.Location.X + buttonFlag.Width, buttonFlag.Location.Y);
            comboBox.Font = new Font("Arial", 16, FontStyle.Bold);
            comboBox.Items.Add("Новичок");
            comboBox.Items.Add("Любитель");
            comboBox.Items.Add("Проффесионал");
            comboBox.SelectedIndex = index;
            Controls.Add(comboBox);
            
            pole = new int[row,col];

            if (index == 0)
            {

                for (int i = 0; i < row; i++)
                {
                    for (int j = 0; j < col; j++)
                    {
                        for (int k = 0; k < n; k++)
                        {
                            if (4 * i + j == 4 * randi[k] + randj[k])
                            {
                                pole[i, j] = -1;
                                if (i != 0 && j != 0 && pole[i - 1, j - 1] > -1)
                                    pole[i - 1, j - 1] += 1;

                                if (i != 0 && pole[i - 1, j] > -1)
                                    pole[i - 1, j] += 1;

                                if (i != 0 && j != col - 1 && pole[i - 1, j + 1] > -1)
                                    pole[i - 1, j + 1] += 1;

                                if (j != col - 1 && pole[i, j + 1] > -1)
                                    pole[i, j + 1] += 1;

                                if (i != row - 1 && j != col - 1 && pole[i + 1, j + 1] > -1)
                                    pole[i + 1, j + 1] += 1;

                                if (i != row - 1 && pole[i + 1, j] > -1)
                                    pole[i + 1, j] += 1;

                                if (i != row - 1 && j != 0 && pole[i + 1, j - 1] > -1)
                                    pole[i + 1, j - 1] += 1;

                                if (j != 0 && pole[i, j - 1] > -1)
                                    pole[i, j - 1] += 1;

                                randi[k] = -1;
                                randj[k] = -1;
                                break;
                            }
                        }
                    }
                }
            }
            else
            {
                for (int k = 0; k < n; k++)
                {
                    int i = randi[k];
                    int j = randj[k];
                    if (pole[randi[k], randj[k]] == -1)
                    {
                        for (int i1 = 0; i1 < row; i1++)
                        {
                            int j1 = Randomly(j);
                            if (pole[Randomly(i1), j1] != -1)
                            {
                                i = Randomly(i1);
                                j = j1;
                                break;
                            }
                        }
                    }

                    pole[i, j] = -1;
                    if (i != 0 && j != 0 && pole[i - 1, j - 1] > -1)
                        pole[i - 1, j - 1] += 1;

                    if (i != 0 && pole[i - 1, j] > -1)
                        pole[i - 1, j] += 1;

                    if (i != 0 && j != col - 1 && pole[i - 1, j + 1] > -1)
                        pole[i - 1, j + 1] += 1;

                    if (j != col - 1 && pole[i, j + 1] > -1)
                        pole[i, j + 1] += 1;

                    if (i != row - 1 && j != col - 1 && pole[i + 1, j + 1] > -1)
                        pole[i + 1, j + 1] += 1;

                    if (i != row - 1 && pole[i + 1, j] > -1)
                        pole[i + 1, j] += 1;

                    if (i != row - 1 && j != 0 && pole[i + 1, j - 1] > -1)
                        pole[i + 1, j - 1] += 1;

                    if (j != 0 && pole[i, j - 1] > -1)
                        pole[i, j - 1] += 1;
                }
            }

//            DataTable dt = new DataTable();
//            for (int i = 0; i < col; i++)
//            {
//                dt.Columns.Add("Column" + i);
//            }
//
//
//            int k = 0;
//            for (int i = 0; i < row; i++)
//            {
//                DataRow r = dt.NewRow();
//                
//                for (int j = 0; j < col; j++)
//                {
//                    if (4 * i + j == 4 * randi[k] + randj[k])
//                    {
//                        r["Column" + j] = -1;
//                        k++;
//                        r[]
//                    }
//                    else r["Column" + j] = 0;
//                }
//                dt.Columns.Add(r);
//            }
//            
//            dataGridView.DataSource = dt;

            //Добавление столбцов и столбцов
            //Задание ширины и высоты таблицы и ячеек
//            DataGridViewColumn[] column = new DataGridViewColumn[col];
//            for (int j = 0; j < col; j++)
//            {
//                column[j] = new DataGridViewButtonColumn();
//            }
//            dataGridView.Columns.AddRange(column);

//            dataGridView.RowCount = row;
//            dataGridView.ColumnCount = col;
//            dataGridView.Height = 0;
//            for (int i = 0; i < row; i++) 
//                dataGridView.Rows[i].Height = h_w;
//
//
//            dataGridView.Width = h_w * col;
//            dataGridView.Height = (h_w + 1) * row;
//            dataGridView.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;
//
//            //стиль таблицы
//            dataGridView.BorderStyle = BorderStyle.None;
//            dataGridView.BackgroundColor = dataGridView.BackColor;
//
//
//            //размещение таблицы по середине
//            dataGridView.Location = new Point(x0 - dataGridView.Width / 2, y0 - dataGridView.Height / 2);
//
//            //добавление таблицы на форму
//            Controls.Add(dataGridView);
//
//            for (int i = 0; i < row; i++)
//            {
//                for (int j = 0; j < col; j++)
//                {
//                    dataGridView.Rows[]
//                }
//            }
            
            button = new Button[row, col];
            int shy = 0;
            for (int i = 0; i < row; i++)
            {
                int shx = 0;
                for (int j = 0; j < col; j++)
                {
                    button[i, j] = new Button();
                    button[i, j].Name = i.ToString() + " " + j.ToString();
                    button[i, j].Click += ButtonOnClick;
                    if (i != row - 1) button[i, j].Size = new Size(h_w, h_w);
                        else button[i, j].Size = new Size(h_w, h_w + 1);
                    button[i, j].Location = new Point(x0 - width / 2 + shx, y0 - height / 2 + shy);
                    shx += h_w;
                    button[i, j].BackColor = Color.DarkSlateGray;
                    button[i, j].FlatStyle = FlatStyle.Standard;
                    button[i, j].FlatAppearance.BorderSize = 3;
                    button[i, j].FlatAppearance.BorderColor = Color.White;
                    button[i, j].MouseEnter += button_MouseEnter;
                    button[i , j].MouseLeave += button_MouseLeave;
                    button[i, j].Font = new Font("Arial", 15);
                    button[i, j].Text = "";
                    Controls.Add(button[i, j]);
                    button[i, j].BringToFront();
                }

                shy += h_w;
            }
            
            buttonMain.Focus();
        }

        public static void Finish()
        {
            for (int i1 = 0; i1 < row; i1++)
            {
                for (int j1 = 0; j1 < col; j1++)
                {
                    if (pole[i1, j1] == -1)
                    {
                        button[i1, j1].FlatStyle = FlatStyle.Popup;
                        button[i1, j1].BackColor = Color.Cornsilk;
                        button[i1, j1].Image = Image.FromFile("C:\\Users\\fesevu\\Desktop\\Лабораторные работы\\Игра\\мина.jpg");
                    }

                    button[i1, j1].Enabled = false;
                }
            }
        }
        private void ButtonOnClick(object sender, EventArgs eventArgs)
        {
            var btn = (Button) sender;
            string[] str = btn.Name.Split(' ');
            int i = int.Parse(str[0]);
            int j = int.Parse(str[1]);
            
            if (textBoxTime.Text == "0")
            {
                timer.Interval = 1000; //интервал между срабатываниями 1000 миллисекунд
                timer.Enabled = true;
                timer.Start();
            }

            if (buttonFlag.Text == "")
            {
                btn.Enabled = false;
                btn.FlatStyle = FlatStyle.Popup;
                btn.BackColor = Color.Cornsilk;

                if (pole[i, j] > 0)
                {
                    btn.Text = pole[i, j].ToString();
                    save_kl--;
                }
                else if (pole[i, j] == -1)
                {
                    timer.Stop();
                    timer.Enabled = false;
                    timer.Dispose();
                    tk = 0;
                    btn.Image = Image.FromFile("C:\\Users\\fesevu\\Desktop\\Лабораторные работы\\Игра\\мина.jpg");
                    buttonMain.Image =
                        Image.FromFile("C:\\Users\\fesevu\\Desktop\\Лабораторные работы\\Игра\\depth.jpg");
                    MessageBox.Show("                Неудача( \n \n Но не время сдаваться!");
                    Finish();
                }
                else if (pole[i, j] == 0)
                {
                    if (i != 0 && j != 0 && pole[i - 1, j - 1] > -1)
                        button[i - 1, j - 1].PerformClick();

                    if (i != 0 && pole[i - 1, j] > -1)
                        button[i - 1, j].PerformClick();

                    if (i != 0 && j != col - 1 && pole[i - 1, j + 1] > -1)
                        button[i - 1, j + 1].PerformClick();

                    if (j != col - 1 && pole[i, j + 1] > -1)
                        button[i, j + 1].PerformClick();

                    if (i != row - 1 && j != col - 1 && pole[i + 1, j + 1] > -1)
                        button[i + 1, j + 1].PerformClick();

                    if (i != row - 1 && pole[i + 1, j] > -1)
                        button[i + 1, j].PerformClick();

                    if (i != row - 1 && j != 0 && pole[i + 1, j - 1] > -1)
                        button[i + 1, j - 1].PerformClick();

                    if (j != 0 && pole[i, j - 1] > -1)
                        button[i, j - 1].PerformClick();

                    save_kl--;
                }
            }
            else if (button[i, j].Text == "")
            {
                button[i, j].Image = Image.FromFile("C:\\Users\\fesevu\\Desktop\\Лабораторные работы\\Игра\\flag.png");
                button[i, j].Text = " ";
                textBoxMine.Text = (int.Parse(textBoxMine.Text) - 1).ToString();
            }
            else
            {
                button[i, j].Image = null;
                button[i, j].Text = "";
                textBoxMine.Text = (int.Parse(textBoxMine.Text) + 1).ToString();
            }

            if (save_kl == 0)
            {
                timer.Stop();
                timer.Enabled = false;
                timer.Dispose();
                tk = 0;
                buttonMain.Image = Image.FromFile("C:\\Users\\fesevu\\Desktop\\Лабораторные работы\\Игра\\win.png");
                Finish();
                MessageBox.Show("                Поздравляю! \n \n Вы лучший минёр!!");
            }
        }

        private void button_MouseEnter(object sender, EventArgs e)
        {
            var btn = (Button)sender;
            btn.FlatAppearance.BorderColor = Color.Blue;
        }

        private void button_MouseLeave(object sender, EventArgs e)
        {
            var btn = (Button)sender;
            btn.FlatAppearance.BorderColor = Color.White;
        }

        private void ButtonMainOnclick(object sender, EventArgs eventArgs)
        {
            Controls.Clear();
            timer.Stop();
            timer.Enabled = false;
            timer.Dispose();
            tk = 0;

            if (comboBox.SelectedIndex == 0)
            {
                row = 9;
                col = 9;
                n = 10;
                index = 0;
            } else if (comboBox.SelectedIndex == 1)
            {
                row = 16;
                col = 16;
                n = 40;
                index = 1;
            } else if (comboBox.SelectedIndex == 2)
            {
                row = 16;
                col = 30;
                n = 99;
                index = 2;
            }
            Form1_Load(sender, null);
        }

        private void ButtonFlagOnclick(object sender, EventArgs eventArgs)
        {
            if (buttonFlag.Text == "")
            {
                buttonFlag.Image = Image.FromFile("C:\\Users\\fesevu\\Desktop\\Лабораторные работы\\Игра\\flag.png");
                buttonFlag.Text = " ";
            }
            else
            {
                buttonFlag.Image = Image.FromFile("C:\\Users\\fesevu\\Desktop\\Лабораторные работы\\Игра\\point.jpg");
                buttonFlag.Text = "";
            }
        }
        
        void timer_Tick(object sender, EventArgs e)
        {
            textBoxTime.Text = (++tk).ToString();
        }
    }
}
