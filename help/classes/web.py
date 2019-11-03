class Web:        
    """
        Clase contenedora de un diccionario con los nombres de las paginas web 
        y las direcciones de los ficheros que representan para ser cargadas 
        desde la clase <HelpWindow>.
    """
    def __init__(self):        
        """            
            Constructor de la clase Web.
        """  
        self.__dicionary = {"GNU Octave": "GNU Octave"}
        self.__model = None

    def set_mode(self, p_model):
        """
            p_model: representa un GtkTreeStore

            Metodo que adiciona de forma estatica los elementos al TreeView del
            Contents de la ayuda.
        """
        iter1 = p_model.append(None, ["GNU Octave"])
        iter2 = p_model.append(None, ["Preface"])
        p_model.append(iter2, ["Acknowledgements"])
        p_model.append(iter2, ["How You Can Contribute to Octave"])
        p_model.append(iter2, ["Distribution"])
        iter3 = p_model.append(None, ["1 A Brief Introduction to Octave"])
        p_model.append(iter3, ["1.1 Running Octave"])
        iter4 = p_model.append(iter3, ["1.2 Simple Examples"])
        p_model.append(iter4, ["1.2.1 Creating a Matrix"])
        p_model.append(iter4, ["1.2.2 Matrix Arithmetic"])
        p_model.append(iter4, ["1.2.3 Solving Linear Equations"])
        p_model.append(iter4, ["1.2.4 Integrating Differential Equations"])
        p_model.append(iter4, ["1.2.5 Producing Graphical Output"])
        p_model.append(iter4, ["1.2.6 Editing What You Have Typed"])
        p_model.append(iter4, ["1.2.7 Help and Documentation"])
        iter5 = p_model.append(iter3, ["1.3 Conventions"])
        p_model.append(iter5, ["1.3.1 Fonts"])
        p_model.append(iter5, ["1.3.2 Evaluation Notation"])
        p_model.append(iter5, ["1.3.3 Printing Notation"])
        p_model.append(iter5, ["1.3.4 Error Messages"])
        iter6 = p_model.append(iter5, ["1.3.5 Format of Descriptions"])
        p_model.append(iter6, ["1.3.5.1 A Sample Function Description"])
        p_model.append(iter6, ["1.3.5.2 A Sample Command Description"])
        p_model.append(iter6, ["1.3.5.3 A Sample Variable Description"])
        iter7 = p_model.append(None, ["2 Getting Started"])
        iter8 = p_model.append(iter7,
                               ["2.1 Invoking Octave from the Command Line"])
        p_model.append(iter8, ["2.1.1 Command Line Options"])
        p_model.append(iter8, ["2.1.2 Startup Files"])
        p_model.append(iter7, ["2.2 Quitting Octave"])
        p_model.append(iter7, ["2.3 Commands for Getting Help"])
        iter9 = p_model.append(iter7, ["2.4 Command Line Editing"])
        p_model.append(iter9, ["2.4.1 Cursor Motion"])
        p_model.append(iter9, ["2.4.2 Killing and Yanking"])
        p_model.append(iter9, ["2.4.3 Commands For Changing Text"])
        p_model.append(iter9, ["2.4.4 Letting Readline Type For You"])
        p_model.append(iter9, ["2.4.5 Commands For Manipulating The History"])
        p_model.append(iter9, ["2.4.6 Customizing readline"])
        p_model.append(iter9, ["2.4.7 Customizing the Prompt"])
        p_model.append(iter9, ["2.4.8 Diary and Echo Commands"])
        p_model.append(iter7, ["2.5 How Octave Reports Errors"])
        p_model.append(iter7, ["2.6 Executable Octave Programs"])
        p_model.append(iter7, ["2.7 Comments in Octave Programs"])
        iter10 = p_model.append(None, ["3 Data Types"])
        iter11 = p_model.append(iter10, ["3.1 Built-in Data Types"])
        p_model.append(iter11, ["3.1.1 Numeric Objects"])
        p_model.append(iter11, ["3.1.2 Missing Data"])
        p_model.append(iter11, ["3.1.3 String Objects"])
        p_model.append(iter11, ["3.1.4 Data Structure Objects"])
        p_model.append(iter11, ["3.1.5 Cell Array Objects"])
        p_model.append(iter10, ["3.2 User-defined Data Types"])
        p_model.append(iter10, ["3.3 Object Sizes"])
        iter12 = p_model.append(None, ["4 Numeric Data Types"])
        iter13 = p_model.append(iter12, ["4.1 Matrices"])
        p_model.append(iter13, ["4.1.1 Empty Matrices"])
        p_model.append(iter12, ["4.2 Ranges"])
        iter14 = p_model.append(iter12, ["4.3 Integer Data Types"])
        p_model.append(iter14, ["4.3.1 Integer Arithmetic"])
        p_model.append(iter12, ["4.4 Bit Manipulations"])
        p_model.append(iter12, ["4.5 Logical Values"])
        p_model.append(iter12, ["4.6 Predicates for Numeric Objects"])
        iter15 = p_model.append(None, ["5 Strings"])
        p_model.append(iter15, ["5.1 Creating Strings"])
        p_model.append(iter15, ["5.2 Comparing Strings"])
        p_model.append(iter15, ["5.3 Manipulating Strings"])
        p_model.append(iter15, ["5.4 String Conversions"])
        p_model.append(iter15, ["5.5 Character Class Functions"])
        iter16 = p_model.append(None, ["6 Data Containers"])
        iter17 = p_model.append(iter16, ["6.1 Data Structures"])
        p_model.append(iter17, ["6.1.1 Structure Arrays"])
        p_model.append(iter17, ["6.1.2 Creating Structures"])
        p_model.append(iter17, ["6.1.3 Manipulating Structures"])
        p_model.append(iter17, ["6.1.4 Processing Data in Structures"])
        iter18 = p_model.append(iter16, ["6.2 Cell Arrays"])
        p_model.append(iter18, ["6.2.1 Creating Cell Array"])
        p_model.append(iter18, ["6.2.2 Indexing Cell Arrays"])
        p_model.append(iter18, ["6.2.3 Cell Arrays of Strings"])
        p_model.append(iter18, ["6.2.4 Processing Data in Cell Arrays"])
        p_model.append(iter16, ["6.3 Comma Separated Lists"])
        iter19 = p_model.append(None, ["7 Variables"])
        p_model.append(iter19, ["7.1 Global Variables"])
        p_model.append(iter19, ["7.2 Persistent Variables"])
        p_model.append(iter19, ["7.3 Status of Variables"])
        p_model.append(iter19, ["7.4 Summary of Built-in Variables"])
        p_model.append(iter19, ["7.5 Defaults from the Environment"])
        iter20 = p_model.append(None, ["8 Expressions"])
        p_model.append(iter20, ["8.1 Index Expressions"])
        iter21 = p_model.append(iter20, ["8.2 Calling Functions"])
        p_model.append(iter21, ["8.2.1 Call by Value"])
        p_model.append(iter21, ["8.2.2 Recursion"])
        p_model.append(iter20, ["8.3 Arithmetic Operators"])
        p_model.append(iter20, ["8.4 Comparison Operators"])
        iter22 = p_model.append(iter20, ["8.5 Boolean Expressions"])
        p_model.append(iter22, ["8.5.1 Element-by-element Boolean Operators"])
        p_model.append(iter22, ["8.5.2 Short-circuit Boolean Operators"])
        p_model.append(iter20, ["8.6 Assignment Expressions"])
        p_model.append(iter20, ["8.7 Increment Operators"])
        p_model.append(iter20, ["8.8 Operator Precedence"])
        iter23 = p_model.append(None, ["9 Evaluation"])
        p_model.append(iter23, ["9.1 Calling a Function by its Name"])
        p_model.append(iter23, ["9.2 Evaluation in a Different Context"])
        iter25 = p_model.append(None, ["10 Statements"])
        p_model.append(iter25, ["10.1 The if Statement"])
        iter26 = p_model.append(iter25, ["10.2 The switch Statement"])
        p_model.append(iter26, ["10.2.1 Notes for the C programmer"])
        p_model.append(iter25, ["10.3 The while Statement"])
        p_model.append(iter25, ["10.4 The do-until Statement"])
        iter27 = p_model.append(iter25, ["10.5 The for Statement"])
        p_model.append(iter27, ["10.5.1 Looping Over Structure Elements"])
        p_model.append(iter25, ["10.6 The break Statement"])
        p_model.append(iter25, ["10.7 The continue Statement"])
        p_model.append(iter25, ["10.8 The unwind_protect Statement"])
        p_model.append(iter25, ["10.9 The try Statement"])
        p_model.append(iter25, ["10.10 Continuation Lines"])
        iter28 = p_model.append(None, ["11 Functions and Script Files"])
        p_model.append(iter28, ["11.1 Defining Functions"])
        p_model.append(iter28, ["11.2 Multiple Return Values"])
        p_model.append(iter28, ["11.3 Variable-length Argument Lists"])
        p_model.append(iter28, ["11.4 Variable-length Return Lists"])
        p_model.append(iter28, ["11.5 Returning From a Function"])
        p_model.append(iter28, ["11.6 Default Arguments"])
        iter29 = p_model.append(iter28, ["11.7 Function Files"])
        p_model.append(iter29, ["11.7.1 Manipulating the load path"])
        p_model.append(iter29, ["11.7.2 Subfunctions"])
        p_model.append(iter29, ["11.7.3 Overloading and Autoloading"])
        p_model.append(iter29, ["11.7.4 Function Locking"])
        p_model.append(iter28, ["11.8 Script Files"])
        iter30 = p_model.append(iter28, 
         ["11.9 Function Handles, Inline Functions, and Anonymous Functions"])
        p_model.append(iter30, ["11.9.1 Function Handles"])
        p_model.append(iter30, ["11.9.2 Anonymous Functions"])
        p_model.append(iter30, ["11.9.3 Inline Functions"])
        p_model.append(iter28, ["11.10 Commands"])
        p_model.append(iter28, 
            ["11.11 Organization of Functions Distributed with Octave"])
        iter31 = p_model.append(None, ["12 Errors and Warnings"])
        iter32 = p_model.append(iter31, ["12.1 Handling Errors"])
        p_model.append(iter32, ["12.1.1 Raising Errors"])
        p_model.append(iter32, ["12.1.2 Catching Errors"])
        iter33 = p_model.append(iter31, ["12.2 Handling Warnings"])
        p_model.append(iter33, ["12.2.1 Issuing Warnings"])
        p_model.append(iter33, ["12.2.2 Enabling and Disabling Warnings"])
        iter34 = p_model.append(None, ["13 Debugging"])
        p_model.append(iter34, ["13.1 Entering Debug Mode"])
        p_model.append(iter34, ["13.2 Breakpoints"])
        p_model.append(iter34, ["13.3 Debug Mode"])
        iter35 = p_model.append(None, ["14 Input and Output"])
        iter36 = p_model.append(iter35, ["14.1 Basic Input and Output"])
        iter37 = p_model.append(iter36, ["14.1.1 Terminal Output"])
        p_model.append(iter37, ["14.1.1.1 Paging Screen Output"])
        p_model.append(iter36, ["14.1.2 Terminal Input"])
        iter38 = p_model.append(iter36, ["14.1.3 Simple File I/O"])
        p_model.append(iter38, ["14.1.3.1 Saving Data on Unexpected Exits"])
        p_model.append(iter36, ["14.1.4 Rational Approximations"])
        iter39 = p_model.append(iter35, ["14.2 C-Style I/O Functions"])
        p_model.append(iter39, ["14.2.1 Opening and Closing Files"])
        p_model.append(iter39, ["14.2.2 Simple Output"])
        p_model.append(iter39, ["14.2.3 Line-Oriented Input"])
        p_model.append(iter39, ["14.2.4 Formatted Output"])
        p_model.append(iter39, ["14.2.5 Output Conversion for Matrices"])
        p_model.append(iter39, ["14.2.6 Output Conversion Syntax"])
        p_model.append(iter39, ["14.2.7 Table of Output Conversions"])
        p_model.append(iter39, ["14.2.8 Integer Conversions"])        
        p_model.append(iter39, ["14.2.9 Floating-Point Conversions"])
        p_model.append(iter39, ["14.2.10 Other Output Conversions"])
        p_model.append(iter39, ["14.2.11 Formatted Input"])
        p_model.append(iter39, ["14.2.12 Input Conversion Syntax"])
        p_model.append(iter39, ["14.2.13 Table of Input Conversions"])
        p_model.append(iter39, ["14.2.14 Numeric Input Conversions"])
        p_model.append(iter39, ["14.2.15 String Input Conversions"])
        p_model.append(iter39, ["14.2.16 Binary I/O"])
        p_model.append(iter39, ["14.2.17 Temporary Files"])
        p_model.append(iter39, ["14.2.18 End of File and Errors"])
        p_model.append(iter39, ["14.2.19 File Positioning"])
        iter40 = p_model.append(None, ["15 Plotting"])
        iter41 = p_model.append(iter40, ["15.1 Plotting Basics"])
        p_model.append(iter41, ["15.1.1 Two-Dimensional Plots"])
        p_model.append(iter41, ["15.1.2 Three-Dimensional Plotting"])
        p_model.append(iter41, ["15.1.3 Plot Annotations"])
        p_model.append(iter41, ["15.1.4 Multiple Plots on One Page"])
        p_model.append(iter41, ["15.1.5 Multiple Plot Windows"])
        p_model.append(iter41, ["15.1.6 Printing Plots"])
        p_model.append(iter41, ["15.1.7 Test Plotting Functions"])
        iter42 = p_model.append(iter40, ["15.2 Advanced Plotting"])
        p_model.append(iter42, ["15.2.1 Graphics Objects"])
        iter43 = p_model.append(iter42, ["15.2.2 Graphics Object Properties"])
        p_model.append(iter43, ["15.2.2.1 Root Figure Properties"])
        p_model.append(iter43, ["15.2.2.2 Figure Properties"])
        p_model.append(iter43, ["15.2.2.3 Axes Properties"])
        p_model.append(iter43, ["15.2.2.4 Line Properties"])
        p_model.append(iter43, ["15.2.2.5 Text Properties"])
        p_model.append(iter43, ["15.2.2.6 Image Properties"])
        p_model.append(iter43, ["15.2.2.7 Patch Properties"])
        p_model.append(iter43, ["15.2.2.8 Surface Properties"])
        p_model.append(iter42, ["15.2.3 Managing Default Properties"])
        p_model.append(iter42, ["15.2.4 Colors"])
        p_model.append(iter42, ["15.2.5 Line Styles"])
        p_model.append(iter42, ["15.2.6 Marker Styles"])
        p_model.append(iter42, ["15.2.7 Interaction with gnuplot"])
        iter44 = p_model.append(None, ["16 Matrix Manipulation"])
        p_model.append(iter44, 
                       ["16.1 Finding Elements and Checking Conditions"])
        p_model.append(iter44, ["16.2 Rearranging Matrices"])
        p_model.append(iter44, ["16.3 Applying a Function to an Array"])
        p_model.append(iter44, ["16.4 Special Utility Matrices"])
        p_model.append(iter44, ["16.5 Famous Matrices"])
        iter45 = p_model.append(None, ["17 Arithmetic"])
        p_model.append(iter45, ["17.1 Utility Functions"])
        p_model.append(iter45, ["17.2 Complex Arithmetic"])
        p_model.append(iter45, ["17.3 Trigonometry"])
        p_model.append(iter45, ["17.4 Sums and Products"])
        p_model.append(iter45, ["17.5 Special Functions"])
        p_model.append(iter45, ["17.6 Coordinate Transformations"])
        p_model.append(iter45, ["17.7 Mathematical Constants"])
        iter46 = p_model.append(None, ["18 Linear Algebra"])
        p_model.append(iter46, ["18.1 Techniques used for Linear Algebra"])
        p_model.append(iter46, ["18.2 Basic Matrix Functions"])
        p_model.append(iter46, ["18.3 Matrix Factorizations"])
        p_model.append(iter46, ["18.4 Functions of a Matrix"])
        iter47 = p_model.append(None, ["19 Nonlinear Equations"])
        iter48 = p_model.append(None, ["20 Sparse Matrices"])
        iter49 = p_model.append(iter48, 
            ["20.1 The Creation and Manipulation of Sparse Matrices"])
        p_model.append(iter49, ["20.1.1 Storage of Sparse Matrices"])
        p_model.append(iter49, ["20.1.2 Creating Sparse Matrices"])
        p_model.append(iter49, 
            ["20.1.3 Finding out Information about Sparse Matrices"])
        iter50 = p_model.append(iter49, 
            ["20.1.4 Basic Operators and Functions on Sparse Matrices"])
        p_model.append(iter50, ["20.1.4.1 Sparse Functions"])
        p_model.append(iter50, 
            ["20.1.4.2 The Return Types of Operators and Functions"])
        p_model.append(iter50, ["20.1.4.3 Mathematical Considerations"])
        p_model.append(iter48, ["20.2 Linear Algebra on Sparse Matrices"])
        p_model.append(iter48, 
            ["20.3 Iterative Techniques applied to sparse matrices"])
        p_model.append(iter48, 
            ["20.4 Real Life Example of the use of Sparse Matrices"])
        iter51 = p_model.append(None, ["21 Numerical Integration"])
        p_model.append(iter51, ["21.1 Functions of One Variable"])
        p_model.append(iter51, ["21.2 Orthogonal Collocation"])
        p_model.append(iter51, ["21.3 Functions of Multiple Variables"])
        iter52 = p_model.append(None, ["22 Differential Equations"])
        p_model.append(iter52, ["22.1 Ordinary Differential Equations"])
        p_model.append(iter52, ["22.2 Differential-Algebraic Equations"])
        iter52 = p_model.append(None, ["23 Optimization"])
        p_model.append(iter52, ["23.1 Linear Programming"])
        p_model.append(iter52, ["23.2 Quadratic Programming"])
        p_model.append(iter52, ["23.3 Nonlinear Programming"])
        p_model.append(iter52, ["23.4 Linear Least Squares"])
        iter53 = p_model.append(None, ["24 Statistics"])
        p_model.append(iter53, ["24.1 Descriptive Statistics"])
        p_model.append(iter53, ["24.2 Basic Statistical Functions"])
        p_model.append(iter53, ["24.3 Statistical Plots"])
        p_model.append(iter53, ["24.4 Tests"])
        p_model.append(iter53, ["24.5 Models"])
        p_model.append(iter53, ["24.6 Distributions"])
        p_model.append(iter53, ["24.7 Random Number Generation"])
        iter54 = p_model.append(None, ["25 Financial Functions"])
        iter55 = p_model.append(None, ["26 Sets"])
        p_model.append(iter55, ["26.1 Set Operations"])
        iter56 = p_model.append(None, ["27 Polynomial Manipulations"])
        p_model.append(iter56, ["27.1 Evaluating Polynomials"])
        p_model.append(iter56, ["27.2 Finding Roots"])
        p_model.append(iter56, ["27.3 Products of Polynomials"])
        p_model.append(iter56, ["27.4 Derivatives and Integrals"])
        p_model.append(iter56, ["27.5 Polynomial Interpolation"])
        p_model.append(iter56, ["27.6 Miscellaneous Functions"])
        iter57 = p_model.append(None, ["28 Interpolation"])
        p_model.append(iter57, ["28.1 One-dimensional Interpolation"])
        p_model.append(iter57, ["28.2 Multi-dimensional Interpolation"])
        iter58 = p_model.append(None, ["29 Geometry"])
        iter59 = p_model.append(iter58, ["29.1 Delaunay Triangulation"])
        p_model.append(iter59, ["29.1.1 Plotting the Triangulation"])
        p_model.append(iter59, ["29.1.2 Identifying points in Triangulation"])
        p_model.append(iter58, ["29.2 Voronoi Diagrams"])
        p_model.append(iter58, ["29.3 Convex Hull"])
        p_model.append(iter58, ["29.4 Interpolation on Scattered Data"])
        iter60 = p_model.append(None, ["30 Control Theory"])
        iter61 = p_model.append(iter60, ["30.1 System Data Structure"])
        p_model.append(iter61, 
                       ["30.1.1 Variables common to all OCST system formats"])
        p_model.append(iter61, ["30.1.2 tf format variables"])
        p_model.append(iter61, ["30.1.3 zp format variables"])
        p_model.append(iter61, ["30.1.4 ss format variables"])	
        iter62 = p_model.append(iter60, 
                ["30.2 System Construction and Interface Functions"])
        p_model.append(iter62, 
                ["30.2.1 Finite impulse response system interface functions"])
        p_model.append(iter62, 
                       ["30.2.2 State space system interface functions"])
        p_model.append(iter62, 
                       ["30.2.3 Transfer function system interface functions"])
        p_model.append(iter62, ["30.2.4 Zero-pole system interface functions"])
        p_model.append(iter62, ["30.2.5 Data structure access functions"]) 
        p_model.append(iter60, ["30.3 System display functions"])
        p_model.append(iter60, ["30.4 Block Diagram Manipulations"])
        p_model.append(iter60, ["30.5 Numerical Functions"])
        p_model.append(iter60, ["30.6 System Analysis-Properties"])
        p_model.append(iter60, ["30.7 System Analysis-Time Domain"])
        p_model.append(iter60, ["30.8 System Analysis-Frequency Domain"])
        p_model.append(iter60, ["30.9 Controller Design"])
        p_model.append(iter60, 
         ["30.10 Miscellaneous Functions (Not yet properly filed/documented)"])
        iter63 = p_model.append(None, ["31 Signal Processing"])
        iter64 = p_model.append(None, ["32 Image Processing"])
        p_model.append(iter64, ["32.1 Loading and Saving Images"])
        p_model.append(iter64, ["32.2 Displaying Images"])
        p_model.append(iter64, ["32.3 Representing Images"])
        p_model.append(iter64, ["32.4 Plotting on top of Images"])
        p_model.append(iter64, ["32.5 Color Conversion"])
        iter65 = p_model.append(None, ["33 Audio Processing"])
        iter66 = p_model.append(None, ["34 Quaternions"])
        iter67 = p_model.append(None, ["35 System Utilities"])
        p_model.append(iter67, ["35.1 Timing Utilities"])
        p_model.append(iter67, ["35.2 Filesystem Utilities"])
        p_model.append(iter67, ["35.3 File Archiving Utilities"])
        p_model.append(iter67, ["35.4 Networking Utilities"])
        p_model.append(iter67, ["35.5 Controlling Subprocesses"])
        p_model.append(iter67, ["35.6 Process, Group, and User IDs"])
        p_model.append(iter67, ["35.7 Environment Variables"])
        p_model.append(iter67, ["35.8 Current Working Directory"])
        p_model.append(iter67, ["35.9 Password Database Functions"])
        p_model.append(iter67, ["35.10 Group Database Functions"])
        p_model.append(iter67, ["35.11 System Information"])
        p_model.append(iter67, ["35.12 Hashing Functions"])
        iter68 = p_model.append(None, ["36 Packages"])
        p_model.append(iter68, ["36.1 Installing and Removing Packages"])
        p_model.append(iter68, ["36.2 Using Packages"])
        p_model.append(iter68, ["36.3 Administrating Packages"])
        iter69 = p_model.append(iter68, ["36.4 Creating Packages"])
        p_model.append(iter69, ["36.4.1 The DESCRIPTION File"])
        p_model.append(iter69, ["36.4.2 The INDEX file"])
        p_model.append(iter69, ["36.4.3 PKG_ADD and PKG_DEL directives"])  	
        iter70 = p_model.append(None, 
                                ["Appendix A Dynamically Linked Functions"])
        iter71 = p_model.append(iter70, ["A.1 Oct-Files"])
        p_model.append(iter71, ["A.1.1 Getting Started with Oct-Files"])
        p_model.append(iter71, ["A.1.2 Matrices and Arrays in Oct-Files"])
        p_model.append(iter71, ["A.1.3 Character Strings in Oct-Files"])
        p_model.append(iter71, ["A.1.4 Cell Arrays in Oct-Files"])
        p_model.append(iter71, ["A.1.5 Structures in Oct-Files"])
        iter72 = p_model.append(iter71, ["A.1.6 Sparse Matrices in Oct-Files"])
        p_model.append(iter72, 
          ["A.1.6.1 The Differences between the Array and Sparse Classes"])
        p_model.append(iter72, 
                       ["A.1.6.2 Creating Sparse Matrices in Oct-Files"])
        p_model.append(iter72, ["A.1.6.3 Using Sparse Matrices in Oct-Files"])
        p_model.append(iter71, 
                       ["A.1.7 Accessing Global Variables in Oct-Files"])
        p_model.append(iter71, 
                       ["A.1.8 Calling Octave Functions from Oct-Files"])
        p_model.append(iter71, ["A.1.9 Calling External Code from Oct-Files"])
        p_model.append(iter71, ["A.1.10 Allocating Local Memory in Oct-Files"])
        p_model.append(iter71, 
                       ["A.1.11 Input Parameter Checking in Oct-Files"])
        p_model.append(iter71, 
                       ["A.1.12 Exception and Error Handling in Oct-Files"])
        p_model.append(iter71, ["A.1.13 Documentation and Test of Oct-Files"])
        iter73 = p_model.append(iter70, ["A.2 Mex-Files"])
        p_model.append(iter73, ["A.2.1 Getting Started with Mex-Files"])
        p_model.append(iter73, 
                       ["A.2.2 Working with Matrices and Arrays in Mex-Files"])
        p_model.append(iter73, ["A.2.3 Character Strings in Mex-Files"])
        p_model.append(iter73, ["A.2.4 Cell Arrays with Mex-Files"])
        p_model.append(iter73, ["A.2.5 Structures with Mex-Files"])
        p_model.append(iter73, ["A.2.6 Sparse Matrices with Mex-Files"])
        p_model.append(iter73, ["A.2.7 Calling Other Functions in Mex-Files"])
        iter74 = p_model.append(iter70, ["A.3 Standalone Programs"])
        iter75 = p_model.append(None, ["Appendix B Test and Demo Functions"])
        p_model.append(iter75, ["B.1 Test Functions"])
        p_model.append(iter75, ["B.2 Demonstration Functions"])
        iter76 = p_model.append(None, ["Appendix C Tips and Standards"])
        p_model.append(iter76, ["C.1 Writing Clean Octave Programs"])
        p_model.append(iter76, ["C.2 Tips for Making Code Run Faster."])
        p_model.append(iter76, ["C.3 Tips on Writing Comments"])
        p_model.append(iter76, 
                       ["C.4 Conventional Headers for Octave Functions"])
        p_model.append(iter76, ["C.5 Tips for Documentation Strings"])
        iter77 = p_model.append(None, ["Appendix D Known Causes of Trouble"])
        p_model.append(iter77, ["D.1 Actual Bugs We Haven't Fixed Yet"])
        p_model.append(iter77, ["D.2 Reporting Bugs"])
        p_model.append(iter77, ["D.3 Have You Found a Bug?"])
        p_model.append(iter77, ["D.4 Where to Report Bugs"])
        p_model.append(iter77, ["D.5 How to Report Bugs"])
        p_model.append(iter77, ["D.6 Sending Patches for Octave"])
        p_model.append(iter77, ["D.7 How To Get Help with Octave"])
        iter78 = p_model.append(None, ["Appendix E Installing Octave"])
        p_model.append(iter78, ["E.1 Installation Problems"])
        iter79 = p_model.append(None, ["Appendix F Emacs Octave Support"])
        p_model.append(iter79, ["F.1 Installing EOS"])
        p_model.append(iter79, ["F.2 Using Octave Mode"])
        p_model.append(iter79, ["F.3 Running Octave From Within Emacs"])
        p_model.append(iter79, ["F.4 Using the Emacs Info Reader for Octave"])
        iter80 = p_model.append(None, 
                                ["Appendix G GNU GENERAL PUBLIC LICENSE"])
        iter81 = p_model.append(None, ["Concept Index"])
        iter82 = p_model.append(None, ["Variable Index"])
        iter83 = p_model.append(None, ["Function Index"])
        iter84 = p_model.append(None, ["Operator Index"])
        self.__model = p_model

    def get_mode(self):
        """
            Retorna: un GtkTreeStore.

            Metodo que retorna el model del treview completamente formado.
        """
        return self.__model

    def set_diccionary(self):
        """
            Metodo que conforma un diccionario de claves-valor para facilitar
            la busqueda y carga de las paginas Web.
        """        
        self.__dicionary = {
        "GNU Octave": "octave", 
        "Preface": "Preface", 
        "Acknowledgements": "Acknowledgements",
        "How You Can Contribute to Octave": "How-You-Can-Contribute-to-Octave", 
        "Distribution": "Distribution", 
        "1 A Brief Introduction to Octave": "Introduction", 
        "1.1 Running Octave": "Running-Octave", 
        "1.2 Simple Examples": "Simple-Examples", 
        "1.2.1 Creating a Matrix": "Simple-Examples", 
        "1.2.2 Matrix Arithmetic": "Simple-Examples",
        "1.2.3 Solving Linear Equations": "Simple-Examples", 
        "1.2.4 Integrating Differential Equations": "Simple-Examples", 
        "1.2.5 Producing Graphical Output": "Simple-Examples", 
        "1.2.6 Editing What You Have Typed": "Simple-Examples", 
        "1.2.7 Help and Documentation": "Simple-Examples", 
        "1.3 Conventions": "Conventions","1.3.1 Fonts": "Fonts", 
        "1.3.2 Evaluation Notation": "Evaluation-Notation", 
        "1.3.3 Printing Notation": "Printing-Notation", 
        "1.3.4 Error Messages": "Error-Messages", 
        "1.3.5 Format of Descriptions": "Format-of-Descriptions", 
        "1.3.5.1 A Sample Function Description": 
        "A-Sample-Function-Description", 
        "1.3.5.2 A Sample Command Description": "A-Sample-Command-Description",
        "1.3.5.3 A Sample Variable Description": 
        "A-Sample-Variable-Description", 
        "2 Getting Started": "Getting-Started", 
        "2.1 Invoking Octave from the Command Line": 
        "Invoking-Octave-from-the-Command-Line", 
        "2.1.1 Command Line Options": "Command-Line-Options", 
        "2.1.2 Startup Files": "Startup-Files",
        "2.2 Quitting Octave": "Quitting-Octave", 
        "2.3 Commands for Getting Help": "Getting-Help",
        "2.4 Command Line Editing": "Command-Line-Editing", 
        "2.4.1 Cursor Motion": "Cursor-Motion", 
        "2.4.2 Killing and Yanking": "Killing-and-Yanking", 
        "2.4.3 Commands For Changing Text": "Commands-For-Text", 
        "2.4.4 Letting Readline Type For You": "Commands-For-Completion", 
        "2.4.5 Commands For Manipulating The History": "Commands-For-History", 
        "2.4.6 Customizing readline": "Customizing-readline", 
        "2.4.7 Customizing the Prompt": "Customizing-the-Prompt", 
        "2.4.8 Diary and Echo Commands": "Diary-and-Echo-Commands", 
        "2.5 How Octave Reports Errors": "Errors", 
        "2.6 Executable Octave Programs": "Executable-Octave-Programs", 
        "2.7 Comments in Octave Programs": "Comments","3 Data Types": 
        "Data-Types", 
        "3.1 Built-in Data Types": "Built_002din-Data-Types", 
        "3.1.1 Numeric Objects": "Numeric-Objects", 
        "3.1.2 Missing Data": "Missing-Data","3.1.3 String Objects": 
        "String-Objects", 
        "3.1.4 Data Structure Objects": "Data-Structure-Objects", 
        "3.1.5 Cell Array Objects": "Cell-Array-Objects", 
        "3.2 User-defined Data Types": "User_002ddefined-Data-Types", 
        "3.3 Object Sizes": "Object-Sizes", 
        "4 Numeric Data Types": "Numeric-Data-Types", 
        "4.1 Matrices": "Matrices", 
        "4.1.1 Empty Matrices": "Empty-Matrices", 
        "4.2 Ranges": "Ranges", 
        "4.3 Integer Data Types": "Integer-Data-Types", 
        "4.3.1 Integer Arithmetic": "Integer-Arithmetic", 
        "4.4 Bit Manipulations": "Bit-Manipulations", 
        "4.5 Logical Values": "Logical-Values", 
        "4.6 Predicates for Numeric Objects": "Predicates-for-Numeric-Objects", 
        "5 Strings": "Strings", 
        "5.1 Creating Strings": "Creating-Strings", 
        "5.2 Comparing Strings": "Comparing-Strings", 
        "5.3 Manipulating Strings": "Manipulating-Strings", 
        "5.4 String Conversions": "String-Conversions", 
        "5.5 Character Class Functions": "Character-Class-Functions", 
        "6 Data Containers": "Data-Containers", 
        "6.1 Data Structures": "Data-Structures", 
        "6.1.1 Structure Arrays": "Structure-Arrays", 
        "6.1.2 Creating Structures": "Creating-Structures",
        "6.1.3 Manipulating Structures": "Manipulating-Structures", 
        "6.1.4 Processing Data in Structures": "Processing-Data-in-Structures", 
        "6.2 Cell Arrays": "Cell-Arrays", 
        "6.2.1 Creating Cell Array": "Creating-Cell-Arrays", 
        "6.2.2 Indexing Cell Arrays": "Indexing-Cell-Arrays", 
        "6.2.3 Cell Arrays of Strings": "Cell-Arrays-of-Strings", 
        "6.2.4 Processing Data in Cell Arrays": 
        "Processing-Data-in-Cell-Arrays", 
        "6.3 Comma Separated Lists": "Comma-Separated-Lists","7 Variables": 
        "Variables", 
        "7.1 Global Variables": "Global-Variables", 
        "7.2 Persistent Variables": "Persistent-Variables", 
        "7.3 Status of Variables": "Status-of-Variables", 
        "7.4 Summary of Built-in Variables": 
        "Summary-of-Built_002din-Variables", 
        "7.5 Defaults from the Environment": "Defaults-from-the-Environment", 
        "8 Expressions": "Expressions", 
        "8.1 Index Expressions": "Index-Expressions", 
        "8.2 Calling Functions": "Calling-Functions", 
        "8.2.1 Call by Value": "Call-by-Value", 
        "8.2.2 Recursion": "Recursion", 
        "8.3 Arithmetic Operators": "Arithmetic-Ops", 
        "8.4 Comparison Operators": "Comparison-Ops", 
        "8.5 Boolean Expressions": "Boolean-Expressions", 
        "8.5.1 Element-by-element Boolean Operators": 
        "Element_002dby_002delement-Boolean-Operators", 
        "8.5.2 Short-circuit Boolean Operators": 
        "Short_002dcircuit-Boolean-Operators", 
        "8.6 Assignment Expressions": "Assignment-Ops", 
        "8.7 Increment Operators": "Increment-Ops", 
        "8.8 Operator Precedence": "Operator-Precedence", 
        "9 Evaluation": "Evaluation", 
        "9.1 Calling a Function by its Name": \
        "Calling-a-Function-by-its-Name", 
        "9.2 Evaluation in a Different Context": 
        "Evaluation-in-a-Different-Context",
        "10 Statements": "Statements", 
        "10.1 The if Statement": "The-if-Statement", 
        "10.2 The switch Statement": "The-switch-Statement", 
        "10.2.1 Notes for the C programmer": "Notes-for-the-C-programmer", 
        "10.3 The while Statement": "The-while-Statement", 
        "10.4 The do-until Statement": "The-do_002duntil-Statement", 
        "10.5 The for Statement": "The-for-Statement", 
        "10.5.1 Looping Over Structure Elements": 
        "Looping-Over-Structure-Elements", 
        "10.6 The break Statement": "The-break-Statement", 
        "10.7 The continue Statement": "The-continue-Statement", 
        "10.8 The unwind_protect Statement": \
        "The-unwind_005fprotect-Statement", 
        "10.9 The try Statement": "The-try-Statement", 
        "10.10 Continuation Lines": "Continuation-Lines", 
        "11 Functions and Script Files": "Functions-and-Scripts",
        "11.1 Defining Functions": "Defining-Functions", 
        "11.2 Multiple Return Values": "Multiple-Return-Values", 
        "11.3 Variable-length Argument Lists": 
        "Variable_002dlength-Argument-Lists", 
        "11.4 Variable-length Return Lists": \
        "Variable_002dlength-Return-Lists", 
        "11.5 Returning From a Function": "Returning-From-a-Function", 
        "11.6 Default Arguments": "Default-Arguments", 
        "11.7 Function Files": "Function-Files", 
        "11.7.1 Manipulating the load path": "Manipulating-the-load-path", 
        "11.7.2 Subfunctions": "Subfunctions", 
        "11.7.3 Overloading and Autoloading": "Overloading-and-Autoloading", 
        "11.7.4 Function Locking": "Function-Locking", 
        "11.8 Script Files": "Script-Files", 
        "11.9 Function Handles, Inline Functions, and Anonymous Functions": 
        "Function-Handles-Inline-Functions-and-Anonymous-Functions", 
        "11.9.1 Function Handles": "Function-Handles", 
        "11.9.2 Anonymous Functions": "Anonymous-Functions", 
        "11.9.3 Inline Functions": "Inline-Functions", 
        "11.10 Commands": "Commands", 
        "11.11 Organization of Functions Distributed with Octave": 
        "Organization-of-Functions", 
        "12 Errors and Warnings": "Errors-and-Warnings", 
        "12.1 Handling Errors": "Handling-Errors", 
        "12.1.1 Raising Errors": "Raising-Errors", 
        "12.1.2 Catching Errors": "Catching-Errors", 
        "12.2 Handling Warnings": "Handling-Warnings", 
        "12.2.1 Issuing Warnings": "Issuing-Warnings", 
        "12.2.2 Enabling and Disabling Warnings": 
        "Enabling-and-Disabling-Warnings", 
        "13 Debugging": "Debugging", 
        "13.1 Entering Debug Mode": "Entering-Debug-Mode", 
        "13.2 Breakpoints": "Breakpoints", 
        "13.3 Debug Mode": "Debug-Mode", 
        "14 Input and Output": "Input-and-Output", 
        "14.1 Basic Input and Output": "Basic-Input-and-Output", 
        "14.1.1 Terminal Output": "Terminal-Output", 
        "14.1.1.1 Paging Screen Output": "Paging-Screen-Output", 
        "14.1.2 Terminal Input": "Terminal-Input", 
        "14.1.3 Simple File I/O": "Simple-File-I_002fO", 
        "14.1.3.1 Saving Data on Unexpected Exits": 
        "Saving-Data-on-Unexpected-Exits", 
        "14.1.4 Rational Approximations": "Rational-Approximations", 
        "14.2 C-Style I/O Functions": "C_002dStyle-I_002fO-Functions", 
        "14.2.1 Opening and Closing Files": "Opening-and-Closing-Files", 
        "14.2.2 Simple Output": "Simple-Output", 
        "14.2.3 Line-Oriented Input": "Line_002dOriented-Input", 
        "14.2.4 Formatted Output": "Formatted-Output", 
        "14.2.5 Output Conversion for Matrices": 
        "Output-Conversion-for-Matrices", 
        "14.2.6 Output Conversion Syntax": "Output-Conversion-Syntax", 
        "14.2.7 Table of Output Conversions": "Table-of-Output-Conversions", 
        "14.2.8 Integer Conversions": "Integer-Conversions", 
        "14.2.9 Floating-Point Conversions": "Floating_002dPoint-Conversions", 
        "14.2.10 Other Output Conversions": "Other-Output-Conversions", 
        "14.2.11 Formatted Input": "Formatted-Input", 
        "14.2.12 Input Conversion Syntax": "Input-Conversion-Syntax", 
        "14.2.13 Table of Input Conversions": "Table-of-Input-Conversions", 
        "14.2.14 Numeric Input Conversions": "Numeric-Input-Conversions", 
        "14.2.15 String Input Conversions": "String-Input-Conversions", 
        "14.2.16 Binary I/O": "Binary-I_002fO", 
        "14.2.17 Temporary Files": "Temporary-Files", 
        "14.2.18 End of File and Errors": "EOF-and-Errors", 
        "14.2.19 File Positioning": "File-Positioning", 
        "15 Plotting": "Plotting", 
        "15.1 Plotting Basics": "Plotting-Basics", 
        "15.1.1 Two-Dimensional Plots": "Two_002dDimensional-Plots", 
        "15.1.2 Three-Dimensional Plotting": "Three_002dDimensional-Plotting", 
        "15.1.3 Plot Annotations": "Plot-Annotations", 
        "15.1.4 Multiple Plots on One Page": "Multiple-Plots-on-One-Page", 
        "15.1.5 Multiple Plot Windows": "Multiple-Plot-Windows", 
        "15.1.6 Printing Plots": "Printing-Plots", 
        "15.1.7 Test Plotting Functions": "Test-Plotting-Functions", 
        "15.2 Advanced Plotting": "Advanced-Plotting", 
        "15.2.1 Graphics Objects": "Graphics-Objects", 
        "15.2.2 Graphics Object Properties": "Graphics-Object-Properties", 
        "15.2.2.1 Root Figure Properties": "Root-Figure-Properties", 
        "15.2.2.2 Figure Properties": "Figure-Properties", 
        "15.2.2.3 Axes Properties": "Axes-Properties", 
        "15.2.2.4 Line Properties": "Line-Properties", 
        "15.2.2.5 Text Properties": "Text-Properties", 
        "15.2.2.6 Image Properties": "Image-Properties", 
        "15.2.2.7 Patch Properties": "Patch-Properties", 
        "15.2.2.8 Surface Properties": "Surface-Properties", 
        "15.2.3 Managing Default Properties": "Managing-Default-Properties",
        "15.2.4 Colors": "Colors", 
        "15.2.5 Line Styles": "Line-Styles", 
        "15.2.6 Marker Styles": "Marker-Styles", 
        "15.2.7 Interaction with gnuplot": "Interaction-with-gnuplot", 
        "16 Matrix Manipulation": "Matrix-Manipulation", 
        "16.1 Finding Elements and Checking Conditions": 
        "Finding-Elements-and-Checking-Conditions", 
        "16.2 Rearranging Matrices": "Rearranging-Matrices", 
        "16.3 Applying a Function to an Array": 
        "Applying-a-Function-to-an-Array", 
        "16.4 Special Utility Matrices": "Special-Utility-Matrices", 
        "16.5 Famous Matrices": "Famous-Matrices", 
        "17 Arithmetic": "Arithmetic", 
        "17.1 Utility Functions": "Utility-Functions", 
        "17.2 Complex Arithmetic": "Complex-Arithmetic", 
        "17.3 Trigonometry": "Trigonometry", 
        "17.4 Sums and Products": "Sums-and-Products", 
        "17.5 Special Functions": "Special-Functions", 
        "17.6 Coordinate Transformations": "Coordinate-Transformations", 
        "17.7 Mathematical Constants": "Mathematical-Constants", 
        "18 Linear Algebra": "Linear-Algebra", 
        "18.1 Techniques used for Linear Algebra": 
        "Techniques-used-for-Linear-Algebra", 
        "18.2 Basic Matrix Functions": "Basic-Matrix-Functions", 
        "18.3 Matrix Factorizations": "Matrix-Factorizations", 
        "18.4 Functions of a Matrix": "Functions-of-a-Matrix", 
        "19 Nonlinear Equations": "Nonlinear-Equations", 
        "20 Sparse Matrices": "Sparse-Matrices", 
        "20.1 The Creation and Manipulation of Sparse Matrices": "Basics", 
        "20.1.1 Storage of Sparse Matrices": "Storage", 
        "20.1.2 Creating Sparse Matrices": "Creation", 
        "20.1.3 Finding out Information about Sparse Matrices": "Information", 
        "20.1.4 Basic Operators and Functions on Sparse Matrices": 
        "Operators-and-Functions", 
        "20.1.4.1 Sparse Functions": "Functions", 
        "20.1.4.2 The Return Types of Operators and Functions": "ReturnType", 
        "20.1.4.3 Mathematical Considerations": "MathConsiderations", 
        "20.2 Linear Algebra on Sparse Matrices": "Sparse-Linear-Algebra", 
        "20.3 Iterative Techniques applied to sparse matrices": 
        "Iterative-Techniques", 
        "20.4 Real Life Example of the use of Sparse Matrices": 
        "Real-Life-Example", 
        "21 Numerical Integration": "Numerical-Integration", 
        "21.1 Functions of One Variable": "Functions-of-One-Variable", 
        "21 Numerical Integration": "Numerical-Integration", 
        "21.1 Functions of One Variable": "Functions-of-One-Variable", 
        "21.2 Orthogonal Collocation": "Orthogonal-Collocation", 
        "21.3 Functions of Multiple Variables": 
        "Functions-of-Multiple-Variables", 
        "22 Differential Equations": "Differential-Equations", 
        "22.1 Ordinary Differential Equations": 
        "Ordinary-Differential-Equations", 
        "22.2 Differential-Algebraic Equations": 
        "Differential_002dAlgebraic-Equations", 
        "23 Optimization": "Optimization", 
        "23.1 Linear Programming": "Linear-Programming", 
        "23.2 Quadratic Programming": "Quadratic-Programming", 
        "23.3 Nonlinear Programming": "Nonlinear-Programming", 
        "23.4 Linear Least Squares": "Linear-Least-Squares", 
        "24 Statistics": "Statistics", 
        "24.1 Descriptive Statistics": "Descriptive-Statistics", 
        "24.2 Basic Statistical Functions": "Basic-Statistical-Functions", 
        "24.3 Statistical Plots": "Statistical-Plots", 
        "24.4 Tests": "Tests", 
        "24.5 Models": "Models", 
        "24.6 Distributions": "Distributions", 
        "24.7 Random Number Generation": "Random-Number-Generation", 
        "25 Financial Functions": "Financial-Functions", 
        "26 Sets": "Sets", 
        "26.1 Set Operations": "Set-Operations", 
        "27 Polynomial Manipulations": "Polynomial-Manipulations", 
        "27.1 Evaluating Polynomials": "Evaluating-Polynomials", 
        "27.2 Finding Roots": "Finding-Roots", 
        "27.3 Products of Polynomials": "Products-of-Polynomials", 
        "27.4 Derivatives and Integrals": "Derivatives-and-Integrals", 
        "27.5 Polynomial Interpolation": "Polynomial-Interpolation", 
        "27.6 Miscellaneous Functions": "Miscellaneous-Functions", 
        "28 Interpolation": "Interpolation", 
        "28.1 One-dimensional Interpolation": 
        "One_002ddimensional-Interpolation", 
        "28.2 Multi-dimensional Interpolation": 
        "Multi_002ddimensional-Interpolation", 
        "29 Geometry": "Geometry", 
        "29.1 Delaunay Triangulation": "Delaunay-Triangulation", 
        "29.1.1 Plotting the Triangulation": "Plotting-the-Triangulation", 
        "29.1.2 Identifying points in Triangulation": 
        "Identifying-points-in-Triangulation", 
        "29.2 Voronoi Diagrams": "Voronoi-Diagrams", 
        "29.3 Convex Hull": "Convex-Hull", 
        "29.4 Interpolation on Scattered Data": 
        "Interpolation-on-Scattered-Data", 
        "30 Control Theory": "Control-Theory", 
        "30.1 System Data Structure": "sysstruct", 
        "30.1.1 Variables common to all OCST system formats": "sysstructvars", 
        "30.1.2 tf format variables": "sysstructtf", 
        "30.1.3 zp format variables": "sysstructzp", 
        "30.1.4 ss format variables": "sysstructss", 
        "30.2 System Construction and Interface Functions": "sysinterface", 
        "30.2.1 Finite impulse response system interface functions": "fir2sys", 
        "30.2.2 State space system interface functions": "ss2sys", 
        "30.2.3 Transfer function system interface functions": "tf2sys", 
        "30.2.4 Zero-pole system interface functions": "zp2sys", 
        "30.2.5 Data structure access functions": "structaccess", 
        "30.3 System display functions": "sysdisp", 
        "30.4 Block Diagram Manipulations": "blockdiag", 
        "30.5 Numerical Functions": "numerical", 
        "30.6 System Analysis-Properties": "sysprop", 
        "30.7 System Analysis-Time Domain": "systime", 
        "30.8 System Analysis-Frequency Domain": "sysfreq", 
        "30.9 Controller Design": "cacsd", 
        "30.10 Miscellaneous Functions (Not yet properly filed/documented)": 
        "misc", 
        "31 Signal Processing": "Signal-Processing", 
        "32 Image Processing": "Image-Processing", 
        "32.1 Loading and Saving Images": "Loading-and-Saving-Images", 
        "32.2 Displaying Images": "Displaying-Images", 
        "32.3 Representing Images": "Representing-Images", 
        "32.4 Plotting on top of Images": "Plotting-on-top-of-Images", 
        "32.5 Color Conversion": "Color-Conversion", 
        "33 Audio Processing": "Audio-Processing", 
        "34 Quaternions": "Quaternions", 
        "35 System Utilities": "System-Utilities", 
        "35.1 Timing Utilities": "Timing-Utilities", 
        "35.2 Filesystem Utilities": "Filesystem-Utilities", 
        "35.3 File Archiving Utilities": "File-Archiving-Utilities", 
        "35.4 Networking Utilities": "Networking-Utilities", 
        "35.5 Controlling Subprocesses": "Controlling-Subprocesses", 
        "35.6 Process, Group, and User IDs": "Process-ID-Information", 
        "35.7 Environment Variables": "Environment-Variables", 
        "35.8 Current Working Directory": "Current-Working-Directory", 
        "35.9 Password Database Functions": "Password-Database-Functions", 
        "35.10 Group Database Functions": "Group-Database-Functions", 
        "35.11 System Information": "System-Information", 
        "35.12 Hashing Functions": "Hashing-Functions", 
        "36 Packages": "Packages", 
        "36.1 Installing and Removing Packages": 
        "Installing-and-Removing-Packages", 
        "36.2 Using Packages": "Using-Packages", 
        "36.3 Administrating Packages": "Administrating-Packages", 
        "36.4 Creating Packages": "Creating-Packages", 
        "36.4.1 The DESCRIPTION File": "The-DESCRIPTION-File", 
        "36.4.2 The INDEX file": "The-INDEX-file", 
        "36.4.3 PKG_ADD and PKG_DEL directives": 
        "PKG_005fADD-and-PKG_005fDEL-directives", 
        "Appendix A Dynamically Linked Functions": 
        "Dynamically-Linked-Functions", 
        "A.1 Oct-Files": "Oct_002dFiles", 
        "A.1.1 Getting Started with Oct-Files": 
        "Getting-Started-with-Oct_002dFiles", 
        "A.1.2 Matrices and Arrays in Oct-Files": 
        "Matrices-and-Arrays-in-Oct_002dFiles", 
        "A.1.3 Character Strings in Oct-Files": 
        "Character-Strings-in-Oct_002dFiles", 
        "A.1.4 Cell Arrays in Oct-Files": "Cell-Arrays-in-Oct_002dFiles", 
        "A.1.5 Structures in Oct-Files": "Structures-in-Oct_002dFiles", 
        "A.1.6 Sparse Matrices in Oct-Files": 
        "Sparse-Matrices-in-Oct_002dFiles", 
        "A.1.6.1 The Differences between the Array and Sparse Classes": 
        "Array-and-Sparse-Differences", 
        "A.1.6.2 Creating Sparse Matrices in Oct-Files": 
        "Creating-Sparse-Matrices-in-Oct_002dFiles", 
        "A.1.6.3 Using Sparse Matrices in Oct-Files": 
        "Using-Sparse-Matrices-in-Oct_002dFiles", 
        "A.1.7 Accessing Global Variables in Oct-Files": 
        "Accessing-Global-Variables-in-Oct_002dFiles", 
        "A.1.8 Calling Octave Functions from Oct-Files": 
        "Calling-Octave-Functions-from-Oct_002dFiles", 
        "A.1.9 Calling External Code from Oct-Files": 
        "Calling-External-Code-from-Oct_002dFiles", 
        "A.1.10 Allocating Local Memory in Oct-Files": 
        "Allocating-Local-Memory-in-Oct_002dFiles", 
        "A.1.11 Input Parameter Checking in Oct-Files": 
        "Input-Parameter-Checking-in-Oct_002dFiles", 
        "A.1.12 Exception and Error Handling in Oct-Files": 
        "Exception-and-Error-Handling-in-Oct_002dFiles", 
        "A.1.13 Documentation and Test of Oct-Files": 
        "Documentation-and-Test-of-Oct_002dFiles", 
        "A.2 Mex-Files": "Mex_002dFiles", 
        "A.2.1 Getting Started with Mex-Files": 
        "Getting-Started-with-Mex_002dFiles", 
        "A.2.2 Working with Matrices and Arrays in Mex-Files": 
        "Working-with-Matrices-and-Arrays-in-Mex_002dFiles", 
        "A.2.3 Character Strings in Mex-Files": 
        "Character-Strings-in-Mex_002dFiles", 
        "A.2.4 Cell Arrays with Mex-Files": "Cell-Arrays-with-Mex_002dFiles", 
        "A.2.5 Structures with Mex-Files": "Structures-with-Mex_002dFiles", 
        "A.2.6 Sparse Matrices with Mex-Files": 
        "Sparse-Matrices-with-Mex_002dFiles", 
        "A.2.7 Calling Other Functions in Mex-Files": 
        "Calling-Other-Functions-in-Mex_002dFiles", 
        "A.3 Standalone Programs": "Standalone-Programs", 
        "Appendix B Test and Demo Functions": "Test-and-Demo-Functions", 
        "B.1 Test Functions": "Test-Functions", 
        "B.2 Demonstration Functions": "Demonstration-Functions", 
        "Appendix C Tips and Standards": "Tips", 
        "C.1 Writing Clean Octave Programs": "Style-Tips", 
        "C.2 Tips for Making Code Run Faster.": "Coding-Tips", 
        "C.3 Tips on Writing Comments": "Comment-Tips", 
        "C.4 Conventional Headers for Octave Functions": "Function-Headers", 
        "C.5 Tips for Documentation Strings": "Documentation-Tips", 
        "Appendix D Known Causes of Trouble": "Trouble", 
        "D.1 Actual Bugs We Haven't Fixed Yet": "Actual-Bugs", 
        "D.2 Reporting Bugs": "Reporting-Bugs", 
        "D.3 Have You Found a Bug?": "Bug-Criteria", 
        "D.4 Where to Report Bugs": "Bug-Lists", 
        "D.5 How to Report Bugs": "Bug-Reporting", 
        "D.6 Sending Patches for Octave": "Sending-Patches", 
        "D.7 How To Get Help with Octave": "Service", 
        "Appendix E Installing Octave": "Installation", 
        "E.1 Installation Problems": "Installation-Problems", 
        "Appendix F Emacs Octave Support": "Emacs", 
        "F.1 Installing EOS": "Installing-EOS", 
        "F.2 Using Octave Mode": "Using-Octave-Mode", 
        "F.3 Running Octave From Within Emacs": 
        "Running-Octave-From-Within-Emacs", 
        "F.4 Using the Emacs Info Reader for Octave": 
        "Using-the-Emacs-Info-Reader-for-Octave", 
        "Appendix G GNU GENERAL PUBLIC LICENSE": "Copying", 
        "Concept Index": "Concept-Index", 
        "Variable Index": "Variable-   Index", 
        "Function Index": "Function-Index", 
        "Operator Index": "Operator-Index", 
        "21 Numerical Integration": "Numerical-Integration", 
        "21.1 Functions of One Variable": "Functions-of-One-Variable", 
        "21.2 Orthogonal Collocation": "Orthogonal-Collocation", 
        "21.3 Functions of Multiple Variables": 
        "Functions-of-Multiple-Variables", 
        "22 Differential Equations": "Differential-Equations", 
        "22.1 Ordinary Differential Equations": 
        "Ordinary-Differential-Equations", 
        "22.2 Differential-Algebraic Equations": 
        "Differential_002dAlgebraic-Equations", 
        "23 Optimization": "Optimization", 
        "23.1 Linear Programming": "Linear-Programming", 
        "23.2 Quadratic Programming": "Quadratic-Programming", 
        "23.3 Nonlinear Programming": "Nonlinear-Programming", 
        "23.4 Linear Least Squares": "Linear-Least-Squares", 
        "24 Statistics": "Statistics", 
        "24.1 Descriptive Statistics": "Descriptive-Statistics", 
        "24.2 Basic Statistical Functions": "Basic-Statistical-Functions", 
        "24.3 Statistical Plots": "Statistical-Plots", 
        "24.4 Tests": "Tests", 
        "24.5 Models": "Models", 
        "24.6 Distributions": "Distributions", 
        "24.7 Random Number Generation": "Random-Number-Generation", 
        "25 Financial Functions": "Financial-Functions", 
        "26 Sets": "Sets", 
        "26.1 Set Operations": "Set-Operations", 
        "27 Polynomial Manipulations": "Polynomial-Manipulations", 
        "27.1 Evaluating Polynomials": "Evaluating-Polynomials", 
        "27.2 Finding Roots": "Finding-Roots", 
        "27.3 Products of Polynomials": "Products-of-Polynomials", 
        "27.4 Derivatives and Integrals": "Derivatives-and-Integrals", 
        "27.5 Polynomial Interpolation": "Polynomial-Interpolation", 
        "27.6 Miscellaneous Functions": "Miscellaneous-Functions", 
        "28 Interpolation": "Interpolation", 
        "28.1 One-dimensional Interpolation": 
        "One_002ddimensional-Interpolation", 
        "28.2 Multi-dimensional Interpolation": 
        "Multi_002ddimensional-Interpolation", 
        "29 Geometry": "Geometry", 
        "29.1 Delaunay Triangulation": "Delaunay-Triangulation", 
        "29.1.1 Plotting the Triangulation": "Plotting-the-Triangulation", 
        "29.1.2 Identifying points in Triangulation": 
        "Identifying-points-in-Triangulation", 
        "29.2 Voronoi Diagrams": "Voronoi-Diagrams", 
        "29.3 Convex Hull": "Convex-Hull", 
        "29.4 Interpolation on Scattered Data": 
        "Interpolation-on-Scattered-Data", 
        "30 Control Theory": "Control-Theory", 
        "30.1 System Data Structure": "sysstruct", 
        "30.1.1 Variables common to all OCST system formats": "sysstructvars", 
        "30.1.2 tf format variables": "sysstructtf", 
        "30.1.3 zp format variables": "sysstructzp", 
        "30.1.4 ss format variables": "sysstructss", 
        "30.2 System Construction and Interface Functions": "sysinterface", 
        "30.2.1 Finite impulse response system interface functions": "fir2sys", 
        "30.2.2 State space system interface functions": "ss2sys", 
        "30.2.3 Transfer function system interface functions": "tf2sys", 
        "30.2.4 Zero-pole system interface functions": "zp2sys", 
        "30.2.5 Data structure access functions": "structaccess", 
        "30.3 System display functions": "sysdisp", 
        "30.4 Block Diagram Manipulations": "blockdiag", 
        "30.5 Numerical Functions": "numerical", 
        "30.6 System Analysis-Properties": "sysprop", 
        "30.7 System Analysis-Time Domain": "systime", 
        "30.8 System Analysis-Frequency Domain": "sysfreq", 
        "30.9 Controller Design": "cacsd", 
        "30.10 Miscellaneous Functions (Not yet properly filed/documented)": 
        "misc", 
        "31 Signal Processing": "Signal-Processing", 
        "32 Image Processing": "Image-Processing", 
        "32.1 Loading and Saving Images": "Loading-and-Saving-Images", 
        "32.2 Displaying Images": "Displaying-Images", 
        "32.3 Representing Images": "Representing-Images", 
        "32.4 Plotting on top of Images": "Plotting-on-top-of-Images", 
        "32.5 Color Conversion": "Color-Conversion", 
        "33 Audio Processing": "Audio-Processing", 
        "34 Quaternions": "Quaternions", 
        "35 System Utilities": "System-Utilities", 
        "35.1 Timing Utilities": "Timing-Utilities", 
        "35.2 Filesystem Utilities": "Filesystem-Utilities", 
        "35.3 File Archiving Utilities": "File-Archiving-Utilities", 
        "35.4 Networking Utilities": "Networking-Utilities", 
        "35.5 Controlling Subprocesses": "Controlling-Subprocesses", 
        "35.6 Process, Group, and User IDs": "Process-ID-Information", 
        "35.7 Environment Variables": "Environment-Variables", 
        "35.8 Current Working Directory": "Current-Working-Directory", 
        "35.9 Password Database Functions": "Password-Database-Functions", 
        "35.10 Group Database Functions": "Group-Database-Functions", 
        "35.11 System Information": "System-Information", 
        "35.12 Hashing Functions": "Hashing-Functions", 
        "36 Packages": "Packages", 
        "36.1 Installing and Removing Packages": 
        "Installing-and-Removing-Packages", 
        "36.2 Using Packages": "Using-Packages", 
        "36.3 Administrating Packages": "Administrating-Packages", 
        "36.4 Creating Packages": "Creating-Packages", 
        "36.4.1 The DESCRIPTION File": "The-DESCRIPTION-File", 
        "36.4.2 The INDEX file": "The-INDEX-file", 
        "36.4.3 PKG_ADD and PKG_DEL directives": 
        "PKG_005fADD-and-PKG_005fDEL-directives", 
        "Appendix A Dynamically Linked Functions": 
        "Dynamically-Linked-Functions", 
        "A.1 Oct-Files": "Oct_002dFiles", 
        "A.1.1 Getting Started with Oct-Files": 
        "Getting-Started-with-Oct_002dFiles", 
        "A.1.2 Matrices and Arrays in Oct-Files": 
        "Matrices-and-Arrays-in-Oct_002dFiles", 
        "A.1.3 Character Strings in Oct-Files": 
        "Character-Strings-in-Oct_002dFiles", 
        "A.1.4 Cell Arrays in Oct-Files": "Cell-Arrays-in-Oct_002dFiles", 
        "A.1.5 Structures in Oct-Files": "Structures-in-Oct_002dFiles", 
        "A.1.6 Sparse Matrices in Oct-Files": 
        "Sparse-Matrices-in-Oct_002dFiles", 
        "A.1.6.1 The Differences between the Array and Sparse Classes": 
        "Array-and-Sparse-Differences", 
        "A.1.6.2 Creating Sparse Matrices in Oct-Files": 
        "Creating-Sparse-Matrices-in-Oct_002dFiles", 
        "A.1.6.3 Using Sparse Matrices in Oct-Files": 
        "Using-Sparse-Matrices-in-Oct_002dFiles", 
        "A.1.7 Accessing Global Variables in Oct-Files": 
        "Accessing-Global-Variables-in-Oct_002dFiles", 
        "A.1.8 Calling Octave Functions from Oct-Files": 
        "Calling-Octave-Functions-from-Oct_002dFiles", 
        "A.1.9 Calling External Code from Oct-Files": 
        "Calling-External-Code-from-Oct_002dFiles", 
        "A.1.10 Allocating Local Memory in Oct-Files": 
        "Allocating-Local-Memory-in-Oct_002dFiles", 
        "A.1.11 Input Parameter Checking in Oct-Files": 
        "Input-Parameter-Checking-in-Oct_002dFiles", 
        "A.1.12 Exception and Error Handling in Oct-Files": 
        "Exception-and-Error-Handling-in-Oct_002dFiles", 
        "A.1.13 Documentation and Test of Oct-Files": 
        "Documentation-and-Test-of-Oct_002dFiles", 
        "A.2 Mex-Files": "Mex_002dFiles", 
        "A.2.1 Getting Started with Mex-Files": 
        "Getting-Started-with-Mex_002dFiles", 
        "A.2.2 Working with Matrices and Arrays in Mex-Files": 
        "Working-with-Matrices-and-Arrays-in-Mex_002dFiles", 
        "A.2.3 Character Strings in Mex-Files": 
        "Character-Strings-in-Mex_002dFiles", 
        "A.2.4 Cell Arrays with Mex-Files": "Cell-Arrays-with-Mex_002dFiles", 
        "A.2.5 Structures with Mex-Files": "Structures-with-Mex_002dFiles", 
        "A.2.6 Sparse Matrices with Mex-Files": 
        "Sparse-Matrices-with-Mex_002dFiles", 
        "A.2.7 Calling Other Functions in Mex-Files": 
        "Calling-Other-Functions-in-Mex_002dFiles", 
        "A.3 Standalone Programs": "Standalone-Programs", 
        "Appendix B Test and Demo Functions": "Test-and-Demo-Functions", 
        "B.1 Test Functions": "Test-Functions", 
        "B.2 Demonstration Functions": "Demonstration-Functions", 
        "Appendix C Tips and Standards": "Tips", 
        "C.1 Writing Clean Octave Programs": "Style-Tips", 
        "C.2 Tips for Making Code Run Faster.": "Coding-Tips", 
        "C.3 Tips on Writing Comments": "Comment-Tips", 
        "C.4 Conventional Headers for Octave Functions": "Function-Headers", 
        "C.5 Tips for Documentation Strings": "Documentation-Tips", 
        "Appendix D Known Causes of Trouble": "Trouble", 
        "D.1 Actual Bugs We Haven't Fixed Yet": "Actual-Bugs", 
        "D.2 Reporting Bugs": "Reporting-Bugs", 
        "D.3 Have You Found a Bug?": "Bug-Criteria", 
        "D.4 Where to Report Bugs": "Bug-Lists", 
        "D.5 How to Report Bugs": "Bug-Reporting", 
        "D.6 Sending Patches for Octave": "Sending-Patches", 
        "D.7 How To Get Help with Octave": "Service", 
        "Appendix E Installing Octave": "Installation", 
        "E.1 Installation Problems": "Installation-Problems", 
        "Appendix F Emacs Octave Support": "Emacs", 
        "F.1 Installing EOS": "Installing-EOS", 
        "F.2 Using Octave Mode": "Using-Octave-Mode", 
        "F.3 Running Octave From Within Emacs": 
        "Running-Octave-From-Within-Emacs", 
        "F.4 Using the Emacs Info Reader for Octave": 
        "Using-the-Emacs-Info-Reader-for-Octave", 
        "Appendix G GNU GENERAL PUBLIC LICENSE": "Copying", 
        "Concept Index": "Concept-Index", 
        "Variable Index": "Variable-Index", 
        "Function Index": "Function-Index", 
        "Operator Index": "Operator-Index"
        }

    def get_page(self, p_texto):    
        """
            Retorna: una cadena de texto.

            Metodo que retorna la direccion de una pagina Web a partir de su 
            titulo.
        """
        return self.__dicionary[p_texto]

    def destroy_diccionary(self):
        """
            Metodo que destruye el diccionario una vez se cambie de sesion de
            trabajo (i.e. Contents, Index o Search Results).
        """
        self.__dicionary = {"GNU Octave": "GNU Octave"}

    def get_diccionario(self):    
        """ 
            Retorna: un diccionario.

            Metodo que retorna el diccionario conformado a partir de los 
            nombres de las paginas web y las direcciones de los ficheros que 
            representan.
        """        
        return self.__dicionary
