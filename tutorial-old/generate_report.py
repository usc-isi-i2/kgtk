import altair as alt
import pandas as pd
import csv
import gzip
from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px
from os import listdir
from os.path import isfile, join

# START OF HTML TEMPLATES

base_template = """
<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">
<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ho+j7jyWK8fNQe+A12Hb8AhRq26LrZ/JpcUGGOn+Y7RsweNrtN/tE3MoK7ZeZDyx" crossorigin="anonymous"></script>

   <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>

{style}

</head>
<body>
<div id="loading-box">
<h3>Loading...</h3>
</div>
  <div id="outer-box" style="display:none">
  <ul class="nav nav-pills mb-3" id="pills-tab" role="tablist">
    <li class="nav-item">
      <a class="nav-link active" id="pills-home-tab" data-toggle="pill" href="#pills-home" role="tab" aria-controls="pills-home" aria-selected="true">Overview</a>
    </li>
    <li class="nav-item">
      <a class="nav-link" id="pills-profile-tab" data-toggle="pill" href="#pills-profile" role="tab" aria-controls="pills-profile" aria-selected="false">Classes</a>
    </li>
    <li class="nav-item">
      <a class="nav-link" id="pills-contact-tab" data-toggle="pill" href="#pills-contact" role="tab" aria-controls="pills-contact" aria-selected="false">Properties</a>
    </li>
  </ul>
  <div class="tab-content" id="pills-tabContent">
    <div class="tab-pane fade show active" id="pills-home" role="tabpanel" aria-labelledby="pills-home-tab">

            {overview_div}

  </div>
    <div class="tab-pane fade" id="pills-profile" role="tabpanel" aria-labelledby="pills-profile-tab">
    <h4 style="color:rgb(55,123,181) ; margin-top:30px;margin-bottom:30px;margin-left:8px" > Main Classes: by {criteria_ranking}</h4>

            {class_div}

    </div>
    <div class="tab-pane fade" id="pills-contact" role="tabpanel" aria-labelledby="pills-contact-tab">

            {property_div}

    </div>
    </div>
  </div>
  </div>

</body>
</html>
"""

style_template = """
<style type="text/css">
  .nav-pills .nav-link.active, .nav-pills .show > .nav-link {
    color: #fff;
    background-color: rgb(55,123,181);
  }
  a,h1 {
    color: rgb(55,123,181);
  }
  body{
    margin:  40px;
    color: gray;
    border: 0.5px solid gray;
    padding: 10px;
    height:100%;
  }
  .table{
    color: gray;
    font-size:12px;

  }

  .btn-primary, .btn-primary:hover, .btn-primary:active, .btn-primary:focus, .btn-primary:visited{
        background-color: rgb(55,123,181);
  }
</style>
  <script  type="text/javascript">
$(document).ready(function() {
    $('#loading-box').hide();
    $('#outer-box').show();


});

   function handle_pop(clicked_id)
    {
        var x = document.getElementById(clicked_id+"/");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
    }
  </script>

"""

# START OVERVIEW TAB TEMPLATE
overview_class_template = """

{overview_summary_div}


{overview_class_summary_div}


"""

overview_summary_template = """

 <div class="card w-100 ">

     <div class="card-body">
         <h5 class="card-title">Summary</h5>
         <div class="row" style="padding:30px;">
         <div class="col-6" >
           {stats_table}
         </div>
          <div class="col-2" >
          </div>
         <div class="col-4">
           {degree_table}
         </div>
       </div >
   </div>

   </div>



"""

overview_class_summary_template = """

<div class="card w-100 ">

 <div class="card-body">
     <h5 class="card-title">Class Summary</h5>
     <div class="row">
     <div class="col-6" style="padding-top:30px;padding-right:10px">
       {class_summary_div_table}
     </div>
     <div class="col-6">
     <div style="float:right">
     {class_summary_div_bar}
     </div>
     </div>
   </div >
   <button class="btn" type="button" data-toggle="collapse" data-target="#collapseExample" aria-expanded="false" aria-controls="collapseExample" style="float:right; margin-top:15px;background-color:rgb(55,123,181); color:white">
Details
</button>
</div>

</div>

<div class="collapse" id="collapseExample" class="card w-75">
 <div class="card card-body">

           <div class="row">
           <div class="col-6" >
           {class_summary_div_pie}
           </div>
           <div class="col-6" style="margin-top:25px">
           {class_summary_div_rank}

           </div>
         </div >

 </div>
</div>



"""

overview_property_template = """

<div class="card w-100 ">
        <div class="card-body">
            <h5 class="card-title">Property Summary <span style="color:rgb(55,123,221)">{property_name}<span></h5>
            <div class="row">
            <div class="col-6"  style="padding-top:40px">

            {property_summary_div_table}

            </div>
            <div class="col-6">
            <div style="float:right">

            {property_summary_div_bar}

            </div>
            </div>
            </div>
            <button onClick="handle_pop(this.id)" id="{file}" class="btn" type="button" style="float:right;margin-top:25px; background-color:rgb(55,123,181);color:white;">
             Details
            </button>

      </div>
  </div>
  <div id="{file_with_slash}" class="card w-100" style="display:none">
    <div class="card card-body">
    <div class="row">
    <div class="col-12">

    {property_summary_div_pie}

    </div>
    </div>
    </div>
  </div>

"""
# END OVERVIEW TAB TEMPLATE

# START OF CLASS TAB TEMPLATE

class_template = """
<div class="card w-100 ">
<h5 style="margin-top: 30px; margin-left:20px"><span style="color:rgb(55,123,181)" >{example_name}</span></h5>

{class_overview_div}
{class_example_div}
{class_property_top_div}
{class_property_incoming_top_div}

</div>

"""

class_overview_template = """

      <div class="card-body">
          <div class="row" style="padding:20px;">
          <div class="col-8" >

            {class_overview_div_table}

          </div>
        </div >
    </div>

"""

class_example_template = """

    <div class="card w-80 " style="border:none">
            <div class="card-body">
                <h6 class="card-title" style="opacity:0.8">{n} Highest Pagerank Instances of <span style="color:rgb(55,123,181)" >{example_name}</span></h6>
                <div class="row">
                <div class="col-6"  style="padding-top:40px">

                {example_summary_div_table}

                </div>
                <div class="col-6">
                <div style="float:right">

                {example_summary_div_bar}

                </div>
                </div>
                </div>
          </div>
      </div>

"""

class_property_incoming_top_template = """
        <div class="card w-80 " style="border:none">
                <div class="card-body">
                    <h6 class="card-title" style="opacity:0.8">{n} Most Popular Incoming Properties on Instances of <span style="color:rgb(55,123,181)" >{example_name}</span> </h6>
                    <div class="row">
                    <div class="col-5"  style="padding-top:40px">

                    {incoming_properties_summary_div_table}

                    </div>
                    <div class="col-7">
                    <div style="float:right">

                    {incoming_properties_summary_div_bar}

                    </div>
                    </div>
                    </div>
                    <button onClick="handle_pop(this.id)" id="incoming{file}" class="btn" type="button" style="float:right;margin-top:15px; background-color:rgb(55,123,181);color:white">
                     Details
                    </button>
              </div>
          </div>
          <div id="incoming{file_with_slash}" class="card w-100" style="display:none;border:none">
            <div class="card card-body">
            <div class="row">
            <div class="col-12">

            {incoming_properties_summary_div_scatter}

            </div>
            </div>
            </div>
          </div>

"""


class_property_top_template = """

    <div class="card w-80 " style="border:none">
                  <div class="card-body">
                      <h6 class="card-title" style="opacity:0.8">{n} Most Popular Properties on Instances of <span style="color:rgb(55,123,181)" >{example_name}</span> </h6>
                      <div class="row">
                      <div class="col-7"  style="padding-top:40px">

                      {properties_summary_div_table}

                      </div>
                      <div class="col-5">
                      <div style="float:right">

                      {properties_summary_div_bar}

                      </div>
                      </div>
                      </div>
                </div>
            </div>

"""

# END OF CLASS TAB TEMPLATE

# START OF PROPERTY TAB TEMPLATE

top_k_property_template = """

{top_k_property_summary_div}
 {example_div}

"""

top_k_property_summary_template = """
<div class="card w-100 ">
        <div class="card-body">
            <h5 class="card-title"><span style="color:rgb(55,123,181)">Top {K} Properties Summary</span></h5>
            <div class="row">
            <div class="col-6"  style="padding-top:40px">

            {property_div_table}

            </div>
            <div class="col-6">
            <div style="float:right">

            {property_div_bar}

            </div>
            </div>
            </div>
            <button onClick="handle_pop(this.id)" id="top_k" class="btn" type="button" style="float:right;margin-top:15px; background-color:rgb(55,123,181); color:white">
             Details
            </button>
      </div>
  </div>
  <div id="top_k/" class="card w-100" style="display:none">
    <div class="card card-body">
    <div class="row">
    <div class="col-12">

    {property_div_pie}

    </div>
    </div>
    </div>
  </div>

"""

example_div_template = """

    <div  class="card w-100" >
      <div class="card card-body">
      <h5 style="margin-bottom:45px;"><span style="color:rgb(55,123,181)">Top {K} Properties Overview</span> </h5>

        {example_tables}

      </div>
    </div>


"""
top_k_property_unit_template = """
      <div class="row">
 <div class="col-6" style="margin-bottom:30px;">
  <h5 style="margin-bottom:40px;"><span style="color:rgb(55,123,181); " >{example_name}<span> </h5>
  <div style="margin-left:25px;">
  {example_div_table}
  </div>
   </div>
   </div>

"""


quantity_template = """

     <div class="card w-100 ">
             <div class="card-body">
                     <h4 class="card-title" style="margin-bottom:30px;"><span style="color:rgb(55,123,181)">Quantity</span></h4>

                     {quantity_div}

</div>
</div>

"""


quantity_unit_template = """

<div class="card w-100 ">
        <div class="card-body">
            <h5 class="card-title"><span style="color:rgb(55,123,181)">{quantity_name}</span></h5>
            <div class="row">
            <div class="col-6"  style="padding-top:40px">

            {quantity_div_table}

            </div>
            <div class="col-6">
            <div style="float:right">

            {quantity_div_bar}

            </div>
            </div>
            </div>
            <button onClick="handle_pop(this.id)" id="{quantity_name}" class="btn" type="button" style="float:right;margin-top:25px; background-color:rgb(55,123,181);color:white">
             Details
            </button>
      </div>
  </div>
  <div id="{quantity_name_with_slash}" class="card w-100" style="display:none">
    <div class="card card-body">
    <div class="row">
    <div class="col-7">
    <h5 style="margin-top:30px;margin-left:30px;">Unit distribution </h5>

    {quantity_div_pie}

    </div>
    <div class="col-5">
    <h5 style="margin-top:30px;">Value distribution for: <span style="color:rgb(55,123,181)">{example_name}</span></h5>

    {quantity_div_histogram}

    </div>
    </div>
    </div>
  </div>


"""


geo_coord_template = """

<div class="card w-100 ">
        <div class="card-body">
            <h4 class="card-title"><span style="color:rgb(55,123,181)">Geo_coord</span></h4>
            <div class="card w-100 " style="margin-top:25px">
            <div class="card-body" >
            <h5 class="card-title"> <span style="color:rgb(55,123,181)">{coordinate_name}</span></h5>
            <div class="row">
                <div class="col-4" >
                </div>
            <div class="col-6" >

            {coordinate_div}

            </div>
                <div class="col-3" >
                </div>
        </div>
        </div>
        </div>
      </div>
  </div>


"""

time_template_template = """

<div class="card w-100 ">
        <div class="card-body">
            <h4 class="card-title"><span style="color:rgb(55,123,181); margin-bottom:30px; ">Time</span></h4>

                {time_div}

      </div>
  </div>
"""

time_div_template = """
            <div class="card w-100 " >
        <div class="card-body" >
            <h5 class="card-title"> <span style="color:rgb(55,123,181)">{time_name}</span></h5>
            <div class="row">

            <div class="col-12" >

            {time_div_histogram}

            </div>

        </div>
        </div>
</div>


"""

# END OF HTML TEMPLATES

WIDTH = 460
HEIGHT = 320

#  START HELPER FUNCTIONS


def create_bar_div(df, X, Y):
    df = df.sort_values(X, ascending=True)
    if X == "Pagerank":
        fig = px.bar(
            df, x=X, y=Y, height=HEIGHT, width=WIDTH, log_x=True, labels={
                "Pagerank": "Log(Pagerank)"}).update_xaxes(
            categoryorder="total descending")
    else:
        fig = px.bar(
            df,
            x=X,
            y=Y,
            height=HEIGHT,
            width=WIDTH).update_xaxes(
            categoryorder="total descending")
    fig.update_traces(marker_color='rgb(55,123,181)')
    fig.update_layout(yaxis_type='category')
    fig.update_layout(
        margin=dict(l=220, r=0)
    )
    fig.update_traces(textposition='outside', textfont_size=1)
    fig.update_layout(
        uniformtext_minsize=3,
        uniformtext_mode='show',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(
            size=8,
            color="gray"))
    return plot(fig, output_type='div', include_plotlyjs=False)


def create_table(df):

    if df.empty:
        len_val = 1
    else:
        len_val = len(df)

    table_html = """  <table class="table table-striped table-bordered table-sm table-responsive-sm"><thead><tr>"""
    link_list = []

    link_present = False
    if 'Link' in df.columns:
        link_list = df.Link.tolist()
        df = df.drop("Link", axis=1)
        link_present = True

    columns = list(df)
    for header in columns:
        table_html += """<th scope="col">""" + header + "</th>"

    table_html += "<tr><thead><tbody>"

    list_index = 0

    for row in df.itertuples():
        table_html += "<tr>"
        val = str(row[1])
        if(link_present):
            node_name = str(link_list[list_index]).split("/")[-1]
            val = "<a href=" + str(link_list[list_index]) + " title= " + str(
                node_name) + " target=" + "_blank" + " >" + val + "</a>"
            list_index += 1

        table_html += """<td scope="row" ><div style="height:20px;width:100%">""" + \
            val + "</div></td>"
        for val in row[2:]:
            if isinstance(val, float):

                val = '{:.4g}'.format(val)
            val = str(val)
            if val.isnumeric():
                val = format(int(val), ",")
            table_html += """<td scope="row" style="max-width:380px;"><div style="height:20px; overflow:hidden; text-align:right">""" + val + "</div></td>"
        table_html += "</tr>"

    table_html += "</tbody></table>"

    return {"table_html": table_html, "len_val": len_val}


def create_desc_table(df):

    if df.empty:
        len_val = 1
    else:
        len_val = len(df)

    table_html = """"""

    for row in df.itertuples():
        table_html += """<div ><div style="font-size:0.85rem;font-weight:550; width:35%;color:rgb(55,123,181);text-align:left;float:left;">"""
        val = row[1]
        if pd.isnull(val):
            val=""
        table_html += str(val)
        table_html += """</div> <div style="font-size:0.80rem;text-align:left; white-space: nowrap;
        width:65%;float:right;overflow:hidden;text-overflow: ellipsis;">"""
        val = row[2]
        if pd.isnull(val):
            val=""
        elif isinstance(val, float):
            val = '{:.4g}'.format(val)
        val = str(val)
        if val.isnumeric():
            val = format(int(val), ",")

        table_html += str(val)
        table_html += "</div></div></br>"

    return {"table_html": table_html, "len_val": len_val}


# END HELPER FUNCTIONS

def run(profiler_files_path):
    # OVERVIEW SECTION

    overview_property_file_list = []
    class_summary_file = ""
    stats_file = ""
    degree_file = ""
    quantity_file = ""

    for f in listdir(f'{profiler_files_path}/overview'):
        if isfile(join(f'{profiler_files_path}/overview', f)):
            if(len(f.split(".")) < 1 or f.split(".")[-1] != "tsv" or f.split(".")[0] != "Overview"):
                continue
            if(len(f.split(".")) == 4 and f.split(".")[1] == "property"):
                overview_property_file_list.append(
                    join(f'{profiler_files_path}/overview', f))
                if (f.split(".")[2] == "quantity"):
                    quantity_file = join(f'{profiler_files_path}/overview', f)
            elif(len(f.split(".")) == 3 and f.split(".")[1] == "class"):
                class_summary_file = join(f'{profiler_files_path}/overview', f)
            elif(len(f.split(".")) == 3 and f.split(".")[1] == "nodes"):
                stats_file = join(f'{profiler_files_path}/overview', f)
            elif(len(f.split(".")) == 3 and f.split(".")[1] == "degree"):
                degree_file = join(f'{profiler_files_path}/overview', f)

    try:
        df = pd.read_csv(stats_file, sep='\t', index_col=[0])
        if df.empty:
            raise Exception("DF Empty")
        stats_table = create_table(df)["table_html"]
    except BaseException:
        stats_table = ""

    try:
        df = pd.read_csv(degree_file, sep='\t', index_col=[0])
        if df.empty:
            raise Exception("DF Empty")
        degree_table = create_table(df)["table_html"]
    except BaseException:
        degree_table = ""

    if degree_table == "" and stats_table == "":
        overview_summary_div = ""
    else:
        overview_summary_div = overview_summary_template.format(
            stats_table=stats_table, degree_table=degree_table)

    class_labels_ordered = []
    criteria_ranking = ""
    try:
        df = pd.read_csv(class_summary_file, sep='\t', index_col=[0])
        if df.empty:
            raise Exception("DF Empty")
        try:
            df.sort_values('Pagerank')
            class_summary_div_rank = create_bar_div(
                df, 'Pagerank', 'Class_Label')
            criteria_ranking = "Pagerank"
        except BaseException:
            criteria_ranking = "Number of Instances"
            class_summary_div_rank = ""
        class_label_col = df.loc[:, 'Class_Label']
        class_labels_ordered = class_label_col.values
        class_summary_div_table = create_table(df)["table_html"]
        class_summary_div_bar = create_bar_div(
            df, 'Number of Instances', 'Class_Label')
        fig = px.pie(
            df,
            values='Number of Instances',
            names='Class_Label',
            height=360,
            width=440)
        class_summary_div_pie = plot(
            fig, output_type='div', include_plotlyjs=False)
        overview_class_summary_div = overview_class_summary_template.format(
            class_summary_div_table=class_summary_div_table,
            class_summary_div_bar=class_summary_div_bar,
            class_summary_div_pie=class_summary_div_pie,
            class_summary_div_rank=class_summary_div_rank)
    except BaseException:
        overview_class_summary_div = ""

    overview_class_div = overview_class_template.format(
        overview_class_summary_div=overview_class_summary_div,
        overview_summary_div=overview_summary_div)

    overview_property_div = ""
    id = 0
    for file in overview_property_file_list:
        try:
            property_name = file.split(".")[2]
            id = id + 1
            df = pd.read_csv(file, sep='\t', index_col=[0])
            if df.empty:
                continue
            property_summary_table = create_table(df)
            property_summary_div_table = property_summary_table["table_html"]
            property_summary_div_bar = create_bar_div(
                df, 'Number_of_Statements', 'Property_Label')
            fig = px.pie(
                df,
                values='Number_of_Statements',
                names='Property_Label',
                title='Statement Distribution')
            property_summary_div_pie = plot(
                fig, output_type='div', include_plotlyjs=False)
            file_with_slash = str(id) + """/"""
            file = str(id)
            overview_property_div += overview_property_template.format(
                property_summary_div_table=property_summary_div_table,
                property_summary_div_bar=property_summary_div_bar,
                property_summary_div_pie=property_summary_div_pie,
                file=file, file_with_slash=file_with_slash, property_name=property_name)
        except BaseException:
            continue

    overview_div = overview_class_div + overview_property_div

    # CLASS SECTION

    class_files = {}
    for f in listdir(f'{profiler_files_path}/class_overview'):
        if isfile(join(f'{profiler_files_path}/class_overview', f)):
            if(len(f.split(".")) < 1 or f.split(".")[-1] != "tsv" or f.split(".")[0] != "Class_overview"):
                continue
            file_key = f.split(".")[1]

            if file_key not in class_files.keys():
                class_files[file_key] = {}

            if(len(f.split(".")) == 4 and f.split(".")[2] == "examples"):
                class_files[file_key]["examples"] = join(
                    f'{profiler_files_path}/class_overview', f)
            elif(len(f.split(".")) == 4 and f.split(".")[2] == "incoming_properties"):
                class_files[file_key]["properties_incoming"] = join(
                    f'{profiler_files_path}/class_overview', f)
            elif(len(f.split(".")) == 4 and f.split(".")[2] == "outgoing_properties"):
                class_files[file_key]["properties"] = join(
                    f'{profiler_files_path}/class_overview', f)
            elif(len(f.split(".")) == 4 and f.split(".")[2] == "overview"):
                class_files[file_key]["overview"] = join(
                    f'{profiler_files_path}/class_overview', f)

    class_div = ""

    K = 6

    for key in class_labels_ordered:
        key = key.replace(" ", "_")
        key = key.replace("-", "_")

        if key not in class_files:
            continue
        try:
            value = class_files[key]
            df = pd.read_csv(value["overview"], sep='\t', index_col=[0])
            if df.empty:
                raise Exception("DF Empty")
            else:
                class_overview_div_table = create_desc_table(df)["table_html"]

                class_overview_div = class_overview_template.format(
                    class_overview_div_table=class_overview_div_table)
        except Exception as e:
            class_overview_div = ""


        try:
            file = value["examples"]
            example_name = file.split(".")[1]
            df = pd.read_csv(file, sep='\t', index_col=[0], nrows=K)
            if df.empty:
                raise Exception("DF Empty")
            else:
                if 'Pagerank' in df.columns:
                    df = df.sort_values(by='Pagerank', ascending=False)
                    example_summary_div_bar = create_bar_div(
                    df, 'Pagerank', 'Label_')
                else:
                    example_summary_div_bar = ""
                example_summary_div_table = create_table(df)["table_html"]
                if len(df) < K:
                    n = len(df)
                else:
                    n = K
                class_example_div = class_example_template.format(
                    example_summary_div_table=example_summary_div_table,
                    example_summary_div_bar=example_summary_div_bar, n=K, example_name=key)
        except Exception as e:
            class_example_div = ""

        try:
            file = value["properties_incoming"]
            df = pd.read_csv(file, sep='\t', index_col=[0], nrows=K)
            if df.empty:
                raise Exception("DF Empty")
            else:
                incoming_properties_summary_div_table = create_table(df)[
                    "table_html"]
                incoming_properties_summary_div_bar = create_bar_div(
                    df, 'Instances', 'Property Name')
                fig = px.pie(
                    df,
                    values='Instances',
                    names='Property Name',
                    title='Distribution')
                incoming_properties_summary_div_pie = plot(
                    fig, output_type='div', include_plotlyjs=False)
                fig = px.scatter(df, x="Property Name", y="Instances")
                fig.update_xaxes(showticklabels=False, title_text='Property')
                incoming_properties_summary_div_scatter = plot(
                    fig, output_type='div', include_plotlyjs=False)
                f_with_slash = "class" + key + """/"""
                f = "class" + key
                n = 0
                if len(df) < K:
                    n = len(df)
                else:
                    n = K
                class_property_incoming_top_div = class_property_incoming_top_template.format(
                    incoming_properties_summary_div_table=incoming_properties_summary_div_table,
                    incoming_properties_summary_div_bar=incoming_properties_summary_div_bar,
                    incoming_properties_summary_div_pie=incoming_properties_summary_div_pie,
                    incoming_properties_summary_div_scatter=incoming_properties_summary_div_scatter,
                    file=f, file_with_slash=f_with_slash, n=n, example_name=key)
        except Exception as e:
            class_property_incoming_top_div = ""

        try:
            file = value["properties"]
            df = pd.read_csv(file, sep='\t', index_col=[0], nrows=K)
            if df.empty:
                raise Exception("DF Empty")
            else:
                properties_summary_div_table = create_table(df)["table_html"]
                properties_summary_div_bar = create_bar_div(
                    df, 'Instances', 'Property Name')
                properties_summary_percent_div_bar = create_bar_div(
                    df, '% Instances', 'Property Name')
                fig = px.pie(df, values='Instances', names='Property Name')
                properties_summary_div_pie = plot(
                    fig, output_type='div', include_plotlyjs=False)
                if len(df) < K:
                    n = len(df)
                else:
                    n = K
                class_property_top_div = class_property_top_template.format(
                    properties_summary_div_table=properties_summary_div_table,
                    properties_summary_div_bar=properties_summary_div_bar,
                    n=K, example_name=key)
        except Exception as e:
            class_property_top_div = ""

        class_div += class_template.format(
            class_overview_div=class_overview_div,
            class_example_div=class_example_div,
            class_property_top_div=class_property_top_div,
            class_property_incoming_top_div=class_property_incoming_top_div,
            example_name=key)

    # PROPERTIES SECTION

    top_property_file = ""
    top_k_properties = {}
    quantity_dict = {}
    geo_coord_file = ""
    time_files = []
    for f in listdir(f'{profiler_files_path}/property_overview'):
        if isfile(join(f'{profiler_files_path}/property_overview', f)):
            if(len(f.split(".")) < 1 or f.split(".")[-1] != "tsv" or f.split(".")[0] != "Property_overview"):
                continue

            if(len(f.split(".")) == 3 and f.split(".")[1] == "top"):
                top_property_file = join(
                    f'{profiler_files_path}/property_overview', f)
            elif(len(f.split(".")) == 4 and f.split(".")[-2] == "overview"):
                top_k_properties[f.split(".")[1]] = join(
                    f'{profiler_files_path}/property_overview', f)
            elif(f.split(".")[1] == "quantity" or f.split(".")[1] == "time"):
                if (f.split(".")[1] == "quantity"):
                    value = f.split(".")[2]
                    if value not in quantity_dict:
                        quantity_dict[value] = {}
                    if f.split(".")[3] == "units_distribution":
                        quantity_dict[value]["units_distribution"] = join(
                            f'{profiler_files_path}/property_overview', f)
                    else:
                        quantity_dict[value]["value_distribution"] = join(
                            f'{profiler_files_path}/property_overview', f)
                else:
                    if(len(f.split(".")) == 5 and f.split(".")[-2] == "year_distibution"):
                        time_files.append(
                            join(f'{profiler_files_path}/property_overview', f))
            elif (f.find("geo_coord") != -1):
                geo_coord_file = join(
                    f'{profiler_files_path}/property_overview', f)

    try:
        df = pd.read_csv(top_property_file, sep='\t', index_col=[0], nrows=K)
        if df.empty:
            raise Exception("DF Empty")
        property_div_table = create_table(df)["table_html"]
        property_div_bar = create_bar_div(
            df, 'Number_of_Statements', 'Property_Label')
        fig = px.pie(
            df,
            values='Number_of_Statements',
            names='Property_Label',
            title='Statements Distribution')
        property_div_pie = plot(fig, output_type='div', include_plotlyjs=False)
        top_k_property_summary_div = top_k_property_summary_template.format(
            property_div_table=property_div_table,
            property_div_bar=property_div_bar,
            property_div_pie=property_div_pie,
            K=K)
    except BaseException:
        top_k_property_summary_div = ""

    example_list = []
    if 'Property_Label' in df.columns:
        example_list = df.Property_Label.tolist()

    count = 0
    example_tables = ""
    for example_name in example_list:
        try:
            example_name = example_name.replace(" ", "_")
            if example_name in top_k_properties:
                example_file = top_k_properties[example_name]
                df = pd.read_csv(
                    example_file,
                    sep='\t',
                    index_col=[0],
                    nrows=K)
                if df.empty:
                    raise Exception("DF Empty")
                example_div_table = create_desc_table(df)["table_html"]
                example_tables += top_k_property_unit_template.format(
                    example_name=example_name, example_div_table=example_div_table)
                count = count + 1
        except BaseException:
            continue

    if example_tables == "":
        example_div = ""
    else:
        example_div = example_div_template.format(
            K=count, example_tables=example_tables)

    top_k_property_div = top_k_property_template.format(
        top_k_property_summary_div=top_k_property_summary_div,
        example_div=example_div)

    quantity_div = ""

    df = pd.read_csv(quantity_file, sep='\t', index_col=[0])
    property_label_list = []
    if 'Property_Label' in df.columns:
        property_label_list = df.Property_Label.tolist()

    quantity_coord_time_div = ""

    for property_label in property_label_list:
        try:
            k = property_label.replace(" ", "_")

            if k in quantity_dict:
                v = quantity_dict[k]
                df = pd.read_csv(
                    v["units_distribution"],
                    sep='\t',
                    index_col=[0],
                    nrows=3)
                quantity_div_table = create_table(df)["table_html"]
                quantity_div_bar = create_bar_div(
                    df, 'Number_of_Statements', 'Unit')
                fig = px.pie(df, values='Number_of_Statements',
                             names='Unit', height=340, width=420)
                quantity_div_pie = plot(
                    fig, output_type='div', include_plotlyjs=False)
                df = pd.read_csv(v["value_distribution"], sep='\t')
                example_name = v["value_distribution"].split(".")[3]
                fig = px.histogram(
                    df, x="Magnitude", height=340, width=420, nbins=10)
                fig.update_traces(marker_color='rgb(55,123,181)')
                fig.update_layout(
                    uniformtext_minsize=3,
                    uniformtext_mode='show',
                    plot_bgcolor='rgba(0, 0, 0, 0)',
                    paper_bgcolor='rgba(0, 0, 0, 0)',
                    font=dict(
                        size=8,
                        color="gray"))
                quantity_div_histogram = plot(
                    fig, output_type='div', include_plotlyjs=False)
                quantity_name_with_slash = k + "/"
                quantity_div += quantity_unit_template.format(
                    quantity_name=k,
                    example_name=example_name,
                    quantity_name_with_slash=quantity_name_with_slash,
                    quantity_div_table=quantity_div_table,
                    quantity_div_bar=quantity_div_bar,
                    quantity_div_pie=quantity_div_pie,
                    quantity_div_histogram=quantity_div_histogram)
                quantity_coord_time_div = quantity_template.format(
                    quantity_div=quantity_div)
        except BaseException:
            continue

    try:
        df = pd.read_csv(geo_coord_file, sep='\t', index_col=[0])
        if df.empty:
            raise Exception("DF Empty")
        fig = px.scatter_mapbox(
            df,
            lat="latitude",
            lon="longitude",
            color_discrete_sequence=["fuchsia"],
            zoom=3,
            height=320)

        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        fig.update_traces(marker_color='rgb(55,123,181)', marker_size=18)
        coordinate_div = plot(fig, output_type='div', include_plotlyjs=False)
        coordinate_name = geo_coord_file.split(".")[2]
        quantity_coord_time_div += geo_coord_template.format(
            coordinate_div=coordinate_div, coordinate_name=coordinate_name)
    except BaseException:
        quantity_coord_time_div += ""

    time_div = ""

    for tf in time_files:
        try:
            time_name = tf.split(".")[2]
            df = pd.read_csv(tf, sep='\t')
            if df.empty:
                raise Exception("DF Empty")
            cols = list(df.columns)
            labels_names = cols[1:]

            fig = px.bar(
                df,
                x=cols[0],
                y=labels_names,
                barmode='stack',
                range_x=[
                    1800,
                    2050],
                width=1000,
                orientation='v')

            fig.update_layout(
                uniformtext_minsize=3,
                barmode='relative',
                bargap=0,
                bargroupgap=0,
                uniformtext_mode='show',
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                font=dict(
                    size=8,
                    color="gray"))

            fig.update_xaxes(title_text='Year')
            time_div_histogram = plot(
                fig, output_type='div', include_plotlyjs=False)
            time_div += time_div_template.format(
                time_name=time_name, time_div_histogram=time_div_histogram)
        except BaseException:
            continue

    time_template = time_template_template.format(time_div=time_div)
    quantity_coord_time_div += time_template
    property_div = top_k_property_div + quantity_coord_time_div

    # FINAL FORMATTING OF BASE TEMPLATE

    with open('report.html', 'w') as f:
        f.write(base_template.format(
            style=style_template,
            overview_div=overview_div,
            class_div=class_div,
            property_div=property_div,
            criteria_ranking=criteria_ranking,
        ))
