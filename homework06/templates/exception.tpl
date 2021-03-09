<!-- news_template.tpl -->
<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.css"></link>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.js"></script>
    </head>
    <body style="background: rgb(34,193,195); background: radial-gradient(circle, rgba(34,193,195,1) 0%, rgba(253,187,45,1) 100%);">
        <div class="ui container" style="font-size: 20px; text-align: center;">Hacker News</div>
            <tfoot class="full-width">
                <h1 class="ui header" style="text-align: center; padding-top: 10px">
                    O-o-oops, something went wrong!
                    <div class="sub header">Got exception: {{ exception or "unknown" }} </div>
                </h1>
                <h1 class="ui header" style="text-align: center; font-size: 150px; margin-top: 200px;">
                    😕
                </h1>   
                <a href="/news" class="fluid small ui bottom attached primary button" style="padding: 15px; margin-top: 200px;">Return to homepage</a>
            </tfoot>
        </table>
        </div>
    </body>
</html>
