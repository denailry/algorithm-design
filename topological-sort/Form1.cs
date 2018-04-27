using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;


namespace topological_sort
{
    public partial class Form1 : Form
    {
        private Graph g1 = new Graph(100);

        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            OpenFileDialog openFileDialog1 = new OpenFileDialog();
            openFileDialog1.InitialDirectory = @"C:\";
            openFileDialog1.Title = "Browse Input File";
            openFileDialog1.CheckFileExists = true;
            openFileDialog1.CheckPathExists = true;
            openFileDialog1.DefaultExt = "txt";
            openFileDialog1.Filter = "Text files (*.txt)|*.txt";
            openFileDialog1.FilterIndex = 2;
            openFileDialog1.RestoreDirectory = true;
            openFileDialog1.ReadOnlyChecked = true;
            openFileDialog1.ShowReadOnly = true;
            if (openFileDialog1.ShowDialog().ToString().Equals("OK"))
            {
                textBox1.Text = openFileDialog1.FileName;
            }
            
            try
            {
                listBox1.Items.Clear();
                using (StreamReader sr = new StreamReader(openFileDialog1.FileName))
                {
                    string line;
                    List<string> g1vertex;
                    while ((line = sr.ReadLine()) != null)
                    {
                        g1vertex = (line.Split('.').ToList<string>())[0].Split(',').ToList<string>();
                        foreach (string value in g1vertex)
                        {
                            string trimmedValue = value.Trim();
                            if (g1.GetVertexIndex(trimmedValue) == -1)
                            {
                                g1.AddVertex(trimmedValue);
                            }
                        }
                        foreach (string value in g1vertex)
                        {
                            string trimmedValue = value.Trim();
                            if (trimmedValue != g1vertex[0])
                            {
                                g1.AddEdge(trimmedValue, g1vertex[0]);
                            }
                        }
                    }
                }
                g1.Display();
                TopologicalSort ts = new TopologicalSort(g1);
                ts.BFS();
                int i = 1;
                foreach(string value in ts.GetResult())
                {
                    listBox1.Items.Add("Semester "+i+": "+value);
                    i++;
                }
            } catch
            {
                textBox1.Text = "The file could not be read!";
            }
        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void textBox3_TextChanged(object sender, EventArgs e)
        {

        }

        private void listBox1_SelectedIndexChanged(object sender, EventArgs e)
        {

        }

        private void button3_Click(object sender, EventArgs e)
        {
            string[] lines = System.IO.File.ReadAllLines("BFS.dat");
           
            Microsoft.Msagl.GraphViewerGdi.GViewer viewer = new Microsoft.Msagl.GraphViewerGdi.GViewer();
            Microsoft.Msagl.Drawing.Graph graph = new Microsoft.Msagl.Drawing.Graph("graph");

            //create the graph content 
            for (int i = 0; i < g1.GetGraphSize(); ++i)
            {
                string vertex = g1.GetVertex(i).data;
                List<string> neighbours = g1.GetNeighbor(vertex);
                if (neighbours.Count == 0)
                {
                    graph.AddNode(vertex);
                } else
                {
                    foreach (var neighbour in neighbours)
                    {
                        graph.AddEdge(vertex, neighbour);
                    }
                }
                graph.FindNode(vertex).LabelText = vertex + " 0";
                graph.FindNode(vertex).Attr.Shape = Microsoft.Msagl.Drawing.Shape.Diamond;
            }
            //bind the graph to the viewer 
            viewer.Graph = graph;
            viewer.Dock = System.Windows.Forms.DockStyle.Fill;

            System.Windows.Forms.Form form = new System.Windows.Forms.Form();
            form.SuspendLayout();
            form.Controls.Add(viewer);
            form.ResumeLayout();
            form.ShowDialog();

            int turn = 0;
            int counter = 0;
            string prevVertex = "";

            const int vertexIndexLength = 2;
            int vertexIndex = 0 - vertexIndexLength;

            int[] vc = new int[g1.GetGraphSize()];
            for (int i = 0; i < g1.GetGraphSize(); ++i)
            {
                vc[i] = 0;
            }

            while (counter < g1.GetGraphSize())
            {
                if ((turn % 2) == 0)
                {
                    vertexIndex += vertexIndexLength;
                    prevVertex = lines[vertexIndex];
                    graph.FindNode(lines[vertexIndex]).Attr.FillColor = Microsoft.Msagl.Drawing.Color.Green;
                    graph.FindNode(lines[vertexIndex]).LabelText = lines[vertexIndex] + " " + vc[g1.GetVertexIndex(prevVertex)].ToString();
                    counter++;
                }
                else
                {
                    List<string> neighbours = lines[vertexIndex + 1].Split(',').ToList<string>();

                    for (int i = 0; i < neighbours.Count - 1; ++i)
                    {
                        int c = vc[g1.GetVertexIndex(neighbours[i])];
                        graph.FindNode(neighbours[i]).Attr.FillColor = Microsoft.Msagl.Drawing.Color.Red;
                        graph.FindNode(neighbours[i]).LabelText = neighbours[i] + " " + (c + 1).ToString();
                        vc[g1.GetVertexIndex(neighbours[i])]++;
                    }
                }
                form.Controls.Add(viewer);
                form.ResumeLayout();
                form.ShowDialog();
                turn++;
            }

            int resultIndex = vertexIndex + vertexIndexLength;
            List<string> resultSequences = lines[resultIndex].Split(',').ToList<string>();
            int rank = 0;
            foreach (var vertex in resultSequences)
            {
                if (vertex.Length != 0)
                {
                    int index = g1.GetVertexIndex(vertex);
                    rank++;
                    graph.FindNode(vertex).Attr.FillColor = Microsoft.Msagl.Drawing.Color.Aqua;
                    graph.FindNode(vertex).LabelText = rank.ToString() + ". " + vertex;
                    List<string> neighbours = g1.GetNeighbor(vertex);
                    foreach (var neighbour in neighbours)
                    {
                        int neighbourIndex = g1.GetVertexIndex(neighbour);
                        vc[neighbourIndex]--;
                        graph.FindNode(neighbour).LabelText = neighbour + " " + vc[neighbourIndex].ToString();
                    }
                    form.Controls.Add(viewer);
                    form.ResumeLayout();
                    form.ShowDialog();
                }
            }
        }

        private void textBox4_TextChanged(object sender, EventArgs e)
        {

        }

        private void textBox2_TextChanged(object sender, EventArgs e)
        {

        }

        private void button2_Click(object sender, EventArgs e)
        {
            TopologicalSort ts = new TopologicalSort(g1);
            ts.DFS();
            //create a form 
            System.Windows.Forms.Form form = new System.Windows.Forms.Form();
            //create a viewer object 
            Microsoft.Msagl.GraphViewerGdi.GViewer viewer = new Microsoft.Msagl.GraphViewerGdi.GViewer();
            //create a graph object 
            Microsoft.Msagl.Drawing.Graph graph = new Microsoft.Msagl.Drawing.Graph("graph");
            //create the graph content 

            int i = 0;
            foreach (Graph.Vertex value1 in g1.GetVertices())
            {
                int j = 0;
                foreach (Graph.Vertex value2 in g1.GetVertices())
                {
                    if (g1.getAdjMatrix()[value1.GetIndex(),value2.GetIndex()] == 1)
                    {
                        graph.AddEdge(g1.GetVertex(i).data, g1.GetVertex(j).data);
                    }
                    j++;
                }
                i++;
            }
            //bind the graph to the viewer 
            viewer.Graph = graph;
            //associate the viewer with the form 
            form.SuspendLayout();
            viewer.Dock = System.Windows.Forms.DockStyle.Fill;
            form.Controls.Add(viewer);
            form.ResumeLayout();
            //show the form 
            form.ShowDialog();
            
            //create the graph content 
            using (StreamReader sr = new StreamReader("DFS.dat"))
            {
                string line;
                List<string> step;
                int count = 0;
                while ((line = sr.ReadLine()) != null)
                {
                    step = line.Split(',').ToList<string>();
                    if (step[0] == "(")
                    {
                        Microsoft.Msagl.Drawing.Node c = graph.FindNode(step[1]);
                        IEnumerable<Microsoft.Msagl.Drawing.Edge> edges = c.OutEdges;
                        foreach (Microsoft.Msagl.Drawing.Edge edge in edges)
                        {
                            if (edge.TargetNode == graph.FindNode(step[2]))
                            {
                                edge.Attr.Color = Microsoft.Msagl.Drawing.Color.Red;
                            }
                        }
                    }
                    else if (step[0] == ">")

                    {
                        graph.FindNode(step[1]).Attr.FillColor = Microsoft.Msagl.Drawing.Color.PaleVioletRed;
                        graph.FindNode(step[1]).LabelText += "/" + step[2].ToString() + ")";
                    }
                    else if (step[0] == "==")
                    {
                        count++;
                        graph.FindNode(step[1]).Attr.FillColor = Microsoft.Msagl.Drawing.Color.Aqua;
                        graph.FindNode(step[1]).LabelText = count + ". " + graph.FindNode(step[1]).LabelText;
                    }
                    else
                    {
                        if (graph.FindNode(step[0]) != null)
                        {
                            graph.FindNode(step[0]).Attr.FillColor = Microsoft.Msagl.Drawing.Color.PaleGreen;
                            graph.FindNode(step[0]).LabelText += " (" + step[1].ToString();
                        }
                    }
                    //bind the graph to the viewer 
                    viewer.Graph = graph;
                    //associate the viewer with the form 
                    form.SuspendLayout();
                    viewer.Dock = System.Windows.Forms.DockStyle.Fill;
                    form.Controls.Add(viewer);
                    form.ResumeLayout();
                    //show the form 
                    form.ShowDialog();
                }
            }
        }
    }
}
