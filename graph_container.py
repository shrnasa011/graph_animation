{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "2d37d0b4-81b6-43b2-b3f8-43d7d2750c29",
   "metadata": {},
   "outputs": [],
   "source": [
    "\n",
    "from manim import *\n",
    "import networkx as nx\n",
    "GREEN_FILL=\"#145A32\"\n",
    "GRAY_OUT=\"#BBBBBB\"\n",
    "\n",
    "class GraphContainerAnimation(Scene):\n",
    "    def construct(self):\n",
    "        vertices=[\"a\",\"b\",\"c\",\"d\",\"e\",\"f\"]\n",
    "        edges=[(\"a\",\"b\"),(\"a\",\"c\"),(\"b\",\"d\"),(\"c\",\"d\"),(\"d\",\"e\"),(\"d\",\"f\"),(\"e\",\"f\")]\n",
    "        G=nx.Graph(); G.add_nodes_from(vertices); G.add_edges_from(edges)\n",
    "        pos=nx.spring_layout(G,seed=2)\n",
    "        layout={v:np.array([4*pos[v][0]-2,3*pos[v][1],0]) for v in vertices}\n",
    "        graph=Graph(vertices,edges,layout=layout,labels=True,\n",
    "            vertex_config={\"radius\":0.18,\"fill_color\":WHITE,\"stroke_color\":BLACK,\"stroke_width\":2})\n",
    "        graph.to_edge(LEFT,buff=.8)\n",
    "        current_I=set(vertices); container=[]\n",
    "        I_tex=MathTex(r\"I=\\{\"+\",\".join(sorted(current_I))+r\"\\}\").scale(.75)\n",
    "        T_tex=MathTex(r\"T=\\emptyset\").scale(.75)\n",
    "        panel=VGroup(Text(\"Input Set\",font_size=28),I_tex,\n",
    "                     Text(\"Container\",font_size=28),T_tex).arrange(DOWN,aligned_edge=LEFT,buff=.35).to_edge(RIGHT)\n",
    "        self.play(Create(graph)); self.play(FadeIn(panel))\n",
    "        while current_I:\n",
    "            H=G.subgraph(current_I); deg=dict(H.degree())\n",
    "            if not deg: break\n",
    "            labels=VGroup(); objs={}\n",
    "            for v,d in deg.items():\n",
    "                lab=Integer(d,color=BLUE).scale(.45).next_to(graph.vertices[v],UP,buff=.12)\n",
    "                labels.add(lab); objs[v]=lab\n",
    "            self.play(FadeIn(labels),run_time=.4)\n",
    "            chosen=max(deg,key=lambda x:(deg[x],x))\n",
    "            self.play(Circumscribe(graph.vertices[chosen],color=YELLOW))\n",
    "            self.play(graph.vertices[chosen].animate.set_fill(GREEN_FILL,opacity=1))\n",
    "            self.play(FadeOut(labels),run_time=.25)\n",
    "            container.append(chosen); current_I.remove(chosen)\n",
    "            newI=MathTex(r\"I=\\{\"+\",\".join(sorted(current_I))+r\"\\}\" if current_I else r\"I=\\emptyset\").scale(.75).move_to(I_tex)\n",
    "            newT=MathTex(r\"T=\\{\"+\",\".join(container)+r\"\\}\").scale(.75).move_to(T_tex)\n",
    "            self.play(Transform(I_tex,newI),Transform(T_tex,newT),run_time=.5)\n",
    "            for u in list(H.neighbors(chosen)):\n",
    "                if u in current_I:\n",
    "                    current_I.remove(u)\n",
    "                    self.play(graph.vertices[u].animate.set_fill(GRAY_OUT,opacity=1),run_time=.2)\n",
    "            for e,m in graph.edges.items():\n",
    "                if chosen in e:\n",
    "                    m.set_stroke(opacity=.2)\n",
    "            self.wait(.2)\n",
    "        self.wait(1)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "bacee5ba-81f7-4eb9-980d-7616e2f8a095",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.14"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
