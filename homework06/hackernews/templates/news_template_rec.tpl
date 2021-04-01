<!-- news_template.tpl -->
<!DOCTYPE html>
<html>
    <head>
        <title>Hacker News</title>
        <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.css"></link>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.js"></script>
    </head>
    <body style="background-color: whitesmoke;">
        <div class="ui container" style="opacity: 0.95;">
        <p></p>
        <div class="ui table" style="font-size: 20px; text-align: center; background-color: #00b9ff;"><a href="/" style="color: #000 !important; text-decoration: none;">Coder's Daily</a></div>
        <table class="ui celled table" style="text-align: center">
            <thead>
                <th>Title</th>
                <th>Author</th>
                <th>Likes</th>
                <th colspan="3">Label</th>
            </thead>
            <tbody>
                %for row in rows:
                <tr style="font-size: 16px;">
                    <td><a href="{{ row.url }}">{{ "😱" + row.title if int(row.points) >= 100 else "🔥" + row.title if int(row.points) >= 10 else row.title }}</a></td>
                    <td>{{ row.author }}</td>
                    <td>{{ row.points }}</td>
                    %if label:
                    <td class="positive"><a href="/add_label/?label=good&id={{ row.id }}">👍</a></td>
                    <td class="active"><a href="/add_label/?label=maybe&id={{ row.id }}">🤔</a></td>
                    <td class="negative"><a href="/add_label/?label=never&id={{ row.id }}">👎</a></td>
                    %else:
                    <%
                    if row.prediction == "good":
                        var = "👍"
                    elif row.prediction == "never":
                        var = "👎"
                    else:
                        var = "🤔"
                    end
                    %>
                    <td><a>{{ var }}</a></td>
                    %end
                </tr>
                %end
            </tbody>
            % if more_button:
            <tfoot class="full-width">
                <tr>
                    <th colspan="7">
                        <a href="/update_news" class="ui right floated small primary button">I Wanna more Hacker News!</a>
                    </th>
                </tr>
            </tfoot>
            % end
        </table>
        </div>
    </body>
</html>
