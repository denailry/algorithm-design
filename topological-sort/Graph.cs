using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace topological_sort
{
    public class Graph
    {
        public class Vertex
        {
            private int index;
            public string data;
            public int GetIndex()
            {
                return index;
            }
            public Vertex(string data, int index)
            {
                this.index = index;
                this.data = data;
            }
        }
        /// <summary>
        /// 4 attributes
        /// a list of vertices (to store node information for each index such as name/text)
        /// a 2D array - our adjacency matrix, stores edges between vertices
        /// a graphSize, Neff size
        /// a maxSize, maximum size of vertices
        /// </summary>
        private List<Vertex> vertices;
        private int graphSize;
        private int maxSize;
        private int[,] adjMatrix;
        private bool rootFound;
        private int rootIndex;
        private int[] directedCount;

        public Graph(int n)
        {
            directedCount = new int[n];
            vertices = new List<Vertex>();
            maxSize = n;//non-zero arrays, add 1
            adjMatrix = new int[maxSize, maxSize];
            for (int i=0; i<maxSize; i++)
            {
                directedCount[0] = 0;
                for (int j = 0; j < maxSize; j++)
                    adjMatrix[i, j] = 0;
            }
            graphSize = 0;
            rootFound = false;
        }
        public int[,] getAdjMatrix()
        {
            return this.adjMatrix;
        }
        public int GetRootIndex()
        {
            if (rootFound)
            {
                return this.rootIndex;
            } else
            {
                int min = maxSize;
                int pos = -1;
                for (int i = 0; i < graphSize; ++i)
                {
                    if (directedCount[i] < min)
                    {
                        min = directedCount[i];
                        pos = i;
                    }
                }
                this.rootIndex = pos;
                rootFound = true;
                return rootIndex;
            }
        }
        public int GetGraphSize()
        {
            return this.graphSize;
        }
        public List<Vertex> GetVertices() {
            return vertices;
        }
        public Vertex GetVertex(int idx) {
            return vertices[idx];
        }
        public int GetVertexIndex(string data) {
            bool found = false;
            int i=0;
            while (i<graphSize && !found) {
                if (data == vertices[i].data)
                    found = true;
                else
                    i++;
            }
            if (found)
                return i;
            else
                return -1;
        }
        public List<string> GetNeighbor(string data) {
            List<string> L = new List<string>();
            int idx = GetVertexIndex(data);
            for (int j=0; j<graphSize; j++) {
                if (adjMatrix[idx, j] == 1)
                    L.Add(GetVertex(j).data);
            }
            return L;
        }
        public void AddVertex(string data)
        {
            Vertex newNode = new Vertex(data, graphSize);
            graphSize++;
            vertices.Add(newNode);
            this.rootFound = false;
        }
        public void AddEdge(string vertexA, string vertexB)
        {
            int i = GetVertexIndex(vertexA);
            int j = GetVertexIndex(vertexB);
            if (i != -1 && j != -1)
            {
                adjMatrix[i, j] = 1;
            }
            rootFound = false;
            directedCount[j]++;
        }
        public void RemoveEdge(string vertexA, string vertexB)
        {
            int i = GetVertexIndex(vertexA);
            int j = GetVertexIndex(vertexB);
            if (i != -1 && j != -1)
            {
                adjMatrix[i, j] = 0;
            }
        }
        public void Display() //displays the adjacency matrix
        {
            Console.WriteLine("***********Adjacency Matrix Representation***********");
            Console.WriteLine("Number of nodes: {0}\n", graphSize - 1);
            Console.Write("\t");
            foreach (Vertex n in vertices)
            {
                Console.Write("{0}\t", n.data);
            }
            Console.WriteLine();//newline for the graph display
            for (int i = 0; i < graphSize; i++)
            {
                Console.Write("{0}\t", vertices[i].data);
                for (int j = 0; j < graphSize; j++)
                {
                    Console.Write("{0}\t", adjMatrix[i, j]);
                }
                Console.WriteLine();
                Console.WriteLine();
            }
        }
    }
}
