<!-- news_template.tpl -->
<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.css"></link>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.js"></script>
    </head>
    <body style="background: rgb(199,138,41); background: linear-gradient(90deg, rgba(199,138,41,1) 27%, rgba(0,212,255,1) 81%);">
        <div class="ui container" style="font-size: 20px; text-align: center; padding-top: 10px;">Hacker News</div>
        <div class="ui container" style="padding-top: 10px; opacity: 0.95;">
        <table class="ui celled table" style="text-align: center">
            <thead>
                <th>Title</th>
                <th>Author</th>
                <th>#Likes</th>
                <th colspan="3">Label</th>
            </thead>
            <tbody>
                %for row in rows:
                <tr style="font-size: 16px;">
                    <td><a href="{{ row.url }}">{{ "😱" + row.title if int(row.points) >= 100 else "🔥" + row.title if int(row.points) >= 10 else row.title }}</a></td>
                    <td>{{ row.author }}</td>
                    <td>{{ row.points }}</td>
                    <td class="positive"><a href="/add_label/?label=good&id={{ row.id }}">👍</a></td>
                    <td class="active"><a href="/add_label/?label=maybe&id={{ row.id }}">🤔</a></td>
                    <td class="negative"><a href="/add_label/?label=never&id={{ row.id }}">👎</a></td>
                </tr>
                %end
            </tbody>
            <tfoot class="full-width">
                <tr>
                    <th colspan="7">
                        <a href="/update_news" class="ui right floated small primary button">I Wanna more Hacker News!</a>
                    </th>
                </tr>
            </tfoot>
        </table>
        </div>
    </body>
</html>
