from manim import *
import numpy as np
import trimesh

config.renderer = "opengl"

def simplify_obj(input_path, output_path, target_faces_ratio = 0.1):
    mesh = trimesh.load(input_path)
    if isinstance(mesh,trimesh.Scene):
        if len(mesh.geometry) == 0:
            raise ValueError("The provided .obj file contains no geometry.")
        mesh = list(mesh.geometry.values())[0]
    
    target_reduction = 1 - target_faces_ratio
    simplified = mesh.simplify_quadric_decimation(int(len(mesh.faces)*target_faces_ratio))
    simplified.export(output_path)
    return output_path


# def parse_obj_fast(file_path):
#     vertices = []
#     faces = []
#     with open(file_path, 'r') as f:
#         for line in f:
#             if line.startswith('v '):
#                 parts = list(map(float,line.strip().split()[1:4]))
#                 vertices.append(parts)
#             elif line.startswith('f '):
#                 face = [int(part.split('/')[0]) - 1 for part in line.strip().split()[1:]]
#                 faces.append(face)
#     return np.array(vertices, dtype = np.float32), np.array(faces, dtype = np.int32)
class introduction(ThreeDScene):
    def construct(self):
        original_path = r"E:\\UNM\\Car-Model\\Car.obj"
        simplified_path = r"E:\\UNM\\Car-Model\\simplified_Car.obj"
        simplify_obj(original_path,simplified_path,target_faces_ratio=0.1)
        
        # vertices, faces = parse_obj_fast(simplified_path)
        
        mesh = OpenGLPMobject.from_obj(simplified_path)
        mesh.set_color(GRAY).set_opacity(0.8)
        
        axes = ThreeDAxes()
        self.add(axes,mesh)
        self.set_camera_orientation(phi=75*DEGREES,theta=30*DEGREES)






class Proof(Scene):
    def construct(self):
        scaling = Text("Scaling",font_size=144)
        self.play(Write(scaling))
        self.wait(2)
        self.play(FadeOut(scaling))

        scaling_graph = Axes(x_range=[-2,5,1],y_range=[-2,5,1],x_length=7,y_length=7,axis_config={"include_tip":True},).shift(LEFT*3)
        square = Square(side_length=1,color=BLUE, fill_opacity=0.5).move_to(scaling_graph.c2p(0.5,0.5))

        def get_vertex_dots():
            return VGroup(*[Dot(point=vertex,color = WHITE) for vertex in square.get_vertices()])
        
        vertex_dots = always_redraw(get_vertex_dots)

        label_xy = always_redraw(lambda:MathTex("(x, y)").next_to(square,UR,buff=0.2))
        sx_arrow = DoubleArrow(start=scaling_graph.c2p(-0.25,-0.5),end=scaling_graph.c2p(3.25,-0.5), color=YELLOW,)
        sx_label = MathTex("s_x=3").next_to(sx_arrow,DOWN,buff=0.2)
        sy_arrow = DoubleArrow(start=scaling_graph.c2p(3.5,-0.25), end=scaling_graph.c2p(3.5,2.25), color=YELLOW,width = 0.1)
        sy_label = MathTex("s_y=2").next_to(sy_arrow,RIGHT,buff=0.2)
        
        self.play(Create(scaling_graph) ,Create(square),Create(vertex_dots))
        self.wait(1)
        self.play(Write(label_xy))
        self.wait(1)

        self.play(square.animate.scale([3,1,1]).move_to(scaling_graph.c2p(0,0),DL))
        self.play(Create(sx_arrow),Write(sx_label))
        self.play(square.animate.scale([1,2,1]).move_to(scaling_graph.c2p(0,0),DL))
        self.play(Create(sy_arrow),Write(sy_label))
        self.wait(2)

        scaling_text = MathTex(r"x'= s_x \cdot x \\"
                               r"y'= s_y \cdot y").shift(RIGHT*4).shift(UP*2)
        self.play(Write(scaling_text))
        self.wait(2)
        scaling_matrix = MathTex(
            r"\begin{bmatrix} x' \\ y' \end{bmatrix} ="
            r"\begin{bmatrix} s_x & 0 \\ 0 & s_y \end{bmatrix}"
            r"\begin{bmatrix} x \\ y \end{bmatrix}"
        ).next_to(scaling_text, DOWN, buff = 1)

        self.play(Transform(scaling_text.copy(), scaling_matrix))
        self.wait(3)
        self.play(square.animate.scale([1/3,1/2,1]).move_to(scaling_graph.c2p(0.0),DL),FadeOut(sx_arrow,sx_label,sy_arrow,sy_label,scaling_text))
        self.wait(1)

        Rotation = Text("Rotation",font_size=144)
        self.play(*[FadeOut(mob)for mob in self.mobjects])
        self.play(Write(Rotation))
        self.wait(2)
        self.play(FadeOut(Rotation))

        self.play(Create(scaling_graph))
        theta = 90 *DEGREES
        r = 4
        alpha = 30 *DEGREES
        start_point = scaling_graph.c2p(0, 0)
        end_point = scaling_graph.c2p(r *np.cos(alpha), r * np.sin(alpha))
        
        lable_xy1 = MathTex(r"(x, y)").next_to(end_point,UR,buff=0.2)
        vector = Arrow(start=start_point,end=end_point,buff=0,color=WHITE)
        
        rotated_end =scaling_graph.c2p(r * np.cos(alpha + theta), r * np.sin(alpha + theta))
        rotated_vector = Arrow(start=start_point, end=rotated_end,buff=0, color=YELLOW)
        
        label_alpha = Angle(
            line1=Line(start_point,scaling_graph.c2p(1,0)),
            line2=vector,
            radius=0.8,
            other_angle=False,
            color=WHITE
            )
        alpha_lable = MathTex(r"\alpha").next_to(label_alpha,RIGHT*0.5,buff=0.1)
        label_theta = Angle (
            line1=  vector,
            line2=rotated_vector,
            radius=0.8,
            other_angle=False,
            color=WHITE
        )
        
        theta_lable = MathTex(r"\theta").next_to(label_theta,UP,buff=0.1)
        label_xy_prime = MathTex(r"(x', y')").next_to(rotated_end,UR,buff=0.2)
        
        self.play(Create(vector),Write(lable_xy1))
        self.play(Create(label_alpha),Write(alpha_lable))
        self.wait(2)

        
        self.play(Rotate(vector.copy(),angle=theta,about_point=scaling_graph.c2p(0,0)), Create(label_theta),Write(theta_lable))
        self.play(Create(rotated_vector), Write(label_xy_prime))
        self.wait(2)

        rotation_equation1 = MathTex(
            r"x = r \cos \alpha \\"
            r"y = r \sin \alpha",
            font_size = 36
        ).shift(RIGHT*3).shift(UP*3)

        rotation_equation2 = MathTex(
            r"x' = r \cos(\alpha + \theta) \\"
            r"y' = r \sin(\alpha + \theta)",
            font_size = 36
        ).next_to(rotation_equation1,DOWN,buff=0.5)

        rotation_equation3 = MathTex(
            r"x' = r \cos(\alpha + \theta) = r \cos\alpha \cos\theta - r \sin\alpha \sin\theta \\"
            r"y' = r \sin(\alpha + \theta) = r \sin\alpha \cos\theta + r \cos\alpha \sin\theta",
            font_size = 36
        ).next_to(rotation_equation1,DOWN,buff=0.5)

        rotation_equation4 = MathTex(
            r"x' = x \cos\theta - y \sin\theta \\"
            r"y' = x \sin\theta + y \cos\theta",
            font_size = 36
        ).next_to(rotation_equation3,DOWN,buff=0.5)

        self.play(Write(rotation_equation1))
        self.wait(1)
        self.play(Write(rotation_equation2))
        self.wait(1)
        self.play(FadeOut(rotation_equation2), Write(rotation_equation3))
        self.wait(1)
        self.play(Transform(Group(rotation_equation3.copy(), rotation_equation1.copy()),rotation_equation4))
        self.wait(2)

        rotation_matrix = MathTex(
            r"\begin{bmatrix} x' \\ y' \end{bmatrix} ="
            r"\begin{bmatrix} \cos\theta & -\sin\theta \\ \sin\theta &\cos\theta \end{bmatrix}"
            r"\begin{bmatrix} x \\ y \end{bmatrix}",
            font_size = 36
        ).next_to(rotation_equation4,DOWN,buff = 0.5)

        self.play(Transform(rotation_equation4.copy(),rotation_matrix))
        self.wait(3)

class Translation(Scene):
    def construct(self):
        translation = Text(r"Translation",font_size=144)
        self.play(Write(translation))
        self.wait(2)
        self.play(FadeOut(translation))

        axes = Axes(x_range=[-2,5,1],y_range=[-2,5,1],x_length=7,y_length=7,axis_config={"include_tip":True},).shift(LEFT*3)
        
        start_point = axes.c2p(0,0)
        dot = Dot(point=start_point,color = WHITE)
        label_xy = MathTex(r"(x, y)").next_to(dot,UL,buff=0.2)

        tx1,ty1 = 3,2
        end_point_1 = axes.c2p(tx1,ty1)
        vector_1 = Arrow(start=start_point, end=end_point_1,buff=0)
        midpoint_1 = interpolate(start_point,end_point_1,alpha=0.6)
        label_t1 = MathTex(r"\vec{t_x}+\vec{t_y}").next_to(midpoint_1,UL,buff=0.2)

        tx2,ty2 = -2,-3
        end_point_2 = axes.c2p(tx1 + tx2, ty1 + ty2)
        vector_2 = Arrow(start=end_point_1,end=end_point_2,buff=0)
        midpoint_2 = interpolate(end_point_1,end_point_2,alpha=0.5)
        label_t2 = MathTex(r"\vec{t_x}'+\vec{t_y}'").next_to(midpoint_2,RIGHT,buff=0.2)
        label_xy1 = MathTex(r"(x', y')").next_to(end_point_1,UR,buff=0.2)
        label_xy2 = MathTex(r"(x'',y'')").next_to(end_point_2,DR,buff=0.2)

        eq1 = MathTex(
            r"x' = x + t_x \\"
            r"y' = y + t_y"
        ).shift(RIGHT * 3).shift(UP * 2)
        eq_scalar = MathTex(r"1 = 1").next_to(eq1,DOWN / 2,buff=0.8)
        eq2 = MathTex(
            r"x' = 1 \cdot x + 0 \cdot y + t_x \\",
            r"y' = 0 \cdot x + 1 \cdot y + t_y \\",
            r"1  = 0 \cdot x + 0 \cdot y + 1"
        ).move_to(eq1)

        translation_matrix = MathTex(
            r"\begin{bmatrix} x' \\ y' \\ 1 \end{bmatrix} =",
            r"\begin{bmatrix} 1 & 0 & t_x \\ 0 & 1 & t_y \\ 0 & 0 & 1 \end{bmatrix}"
            r"\begin{bmatrix} x \\ y \\ 1 \end{bmatrix}"
        ).next_to(eq2,DOWN)

        self.play(Create(axes),Create(dot),Write(label_xy))
        self.wait(1)

        self.play(Create(vector_1),Write(label_t1),dot.animate.move_to(end_point_1),Transform(label_xy.copy(),label_xy1))
        self.wait(1)
        self.play(Create(vector_2),Write(label_t2),dot.animate.move_to(end_point_2),Transform(label_xy1,label_xy2))
        self.wait(2)

        self.play(Write(eq1))
        self.wait(2)

        self.play(Write(eq_scalar))
        self.wait(1)
        self.play(Transform(VGroup(eq1,eq_scalar),eq2))
        self.wait(2)

        self.play(Transform(eq2,translation_matrix))
        self.wait(3)
        
        self.play(*[FadeOut(mob)for mob in self.mobjects])
        self.wait(1)


        s1 = MathTex(
            r"S = \begin{bmatrix} s_x & 0 \\ 0 & s_y \end{bmatrix}",
            font_size = 36
        ).shift(LEFT*4)
        r1 = MathTex(
            r"R = \begin{bmatrix} cos\theta & -sin\theta \\ sin\theta & cos\theta \end{bmatrix}",
            font_size = 36
        )
        t1 = MathTex(
            r"T = \begin{bmatrix} 1 & 0 & t_x \\ 0 & 1 & t_y \\ 0 & 0 & 1\end{bmatrix}",
            font_size = 36
        ).shift(RIGHT*4)

        s2 = MathTex(
            r"S = \begin{bmatrix} s_x & 0 & 0 & 0 \\ 0 & s_y & 0 & 0 \\ 0 & 0 & s_z & 0 \\ 0 & 0 & 0 & 1\end{bmatrix}",
            font_size = 36
        ).shift(LEFT*5)

        rx = MathTex(
            r"R_x = \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & cos\theta & -sin\theta & 0 \\ 0 & sin\theta & cos\theta & 0 \\ 0 & 0 & 0 & 1\end{bmatrix}",
            font_size = 36
        ).shift(UP*2.5)
        ry = MathTex(
            r"Ry = \begin{bmatrix} cos\theta & 0 & sin\theta & 0 \\ 0 & 1 & 0 & 0 \\ -sin\theta & 0 & cos\theta & 0 \\ 0 & 0 & 0 & 1\end{bmatrix}",
            font_size = 36
        )
        rz = MathTex(
            r"R_z = \begin{bmatrix} cos\theta & -sin\theta & 0 & 0 \\ sin\theta & cos\theta & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1\end{bmatrix}",
            font_size = 36
        ).shift(DOWN*2.5)

        t2 = MathTex(
            r"T = \begin{bmatrix} 1 & 0 & 0 & t_x \\ 0 & 1 & 0 & t_y \\ 0 & 0 & 1 & t_z \\ 0 & 0 & 0 & 1\end{bmatrix}",
            font_size = 36
        ).shift(RIGHT*5)

        self.play(Write(s1),Write(r1),Write(t1))
        self.wait(2)
        self.play(Transform(s1,s2),Transform(r1.copy(),rx),Transform(r1.copy(),rz),Transform(r1,ry),Transform(t1,t2))
        self.wait(3)




class Conclusion(Scene):
    def construct(self):   
        p_xy = MathTex(
            r"P_{xy} =",
            r"\begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}"
        ).scale(0.8)
        p_xy.shift(UP * 2)
        self.play(Write(p_xy))
        self.wait(2)
        
        projection_formula = MathTex(
            r"P = R^{-1} P_{xy} R"
        ).scale(0.9)
        projection_formula.next_to(p_xy, DOWN, buff=0.5)
        self.play(Write(projection_formula))
        self.wait(2)
        
        expanded_formula = MathTex(
            r"P =",
            r"R^{-1} ",
            r"\begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}",
            r" R"
        ).scale(0.8)
        expanded_formula.next_to(projection_formula, DOWN, buff=0.5)
        self.play(Write(expanded_formula))
        self.wait(3)
        
        final_projection = MathTex(
            r"P =",
            r"\begin{bmatrix} \cdots & \cdots & \cdots & \cdots \\ \cdots & \cdots & \cdots & \cdots \\ \cdots & \cdots & \cdots & \cdots \\ \cdots & \cdots & \cdots & \cdots \end{bmatrix}"
        ).scale(0.8)
        final_projection.next_to(expanded_formula, DOWN, buff=0.5)
        self.play(Transform(expanded_formula, final_projection))
        self.wait(3)
        
class Smooth3DTo2D(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES)
        axes = ThreeDAxes()
        cube = Cube().move_to([0, 0, 0])
        plane = Square(fill_opacity=0.5, fill_color=BLUE, stroke_color=WHITE)
        plane.rotate_about_origin(PI/4, UP)
        plane.rotate_about_origin(PI/6, RIGHT)
        plane.move_to([0, 0, 0])
        
        self.play(Create(axes), Create(cube), )
        self.wait(2)
        
        projection_matrix = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ])
        projected_cube = cube.copy().apply_matrix(projection_matrix)
        self.play(Transform(cube, projected_cube))
        self.wait(2)
        
        self.move_camera(phi=0 * DEGREES, theta=0 * DEGREES)
        self.wait(2)
        
        self.move_camera(phi=60 * DEGREES, theta=45 * DEGREES)
        self.play(Transform(cube, Cube().move_to([0, 0, 0])))
        self.wait(2)
        
        r_matrix = np.array([
            [np.cos(PI/4), 0, -np.sin(PI/4)],
            [0, 1, 0],
            [np.sin(PI/4), 0, np.cos(PI/4)]
        ])
        self.play(Create(plane))
        transformed_axes = axes.copy().apply_matrix(r_matrix)
        transformed_plane = plane.copy().apply_matrix(r_matrix).move_to([0, 0, 0])
        transformed_cube = cube.copy().apply_matrix(r_matrix)
        
        self.play(Transform(axes, transformed_axes),
                  Transform(plane, transformed_plane),
                  Transform(cube, transformed_cube))
        self.wait(2)
        
        projection_matrix_xz = np.array([
            [1, 0, 0],
            [0, 0, 0],
            [0, 0, 1]
        ])
        projected_cube_custom = transformed_cube.copy().apply_matrix(projection_matrix_xz)
        self.play(Transform(cube, projected_cube_custom))
        self.wait(3)
