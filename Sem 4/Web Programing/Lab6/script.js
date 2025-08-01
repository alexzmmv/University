$(document).ready(function() {
    let draggingElement = null;
    let draggingElementOriginalPosition = null;
    let mouseStartX, mouseStartY;
    let elementStartX, elementStartY;
    let elementWidth, elementHeight;
    let placeholder = null;
    let containerOffset = null;
    
    let itemsList = [];
    
    function loadFromLocalStorage() {
        const savedItems = localStorage.getItem('stackItems');
        if (savedItems) {
            itemsList = JSON.parse(savedItems);
            renderItems();
        }
    }
    
    function saveToLocalStorage() {
        localStorage.setItem('stackItems', JSON.stringify(itemsList));
    }
    
    function addItem(text, pos=null) {
        if(pos===null) {
            itemsList.push({ text: text });
        } else {
            itemsList.splice(pos, 0, { text: text });
        }
        saveToLocalStorage();
        renderItems();
    }
    
    function renderItems() {
        const container = $('#container');
        container.empty();
        
        itemsList.forEach(item => {
            const newItem = $('<div></div>')
                .addClass('stack-item')
                .text(item.text);
            container.append(newItem);
        });
    }
    
    function updateItemsListFromDOM() {
        itemsList = [];
        $('#container .stack-item').each(function() {
            itemsList.push({
                text: $(this).text()
            });
        });
        saveToLocalStorage();
    }
    
    function createPlaceholder(element) {
        const $element = $(element);
        const $placeholder = $('<div></div>')
            .addClass('stack-item placeholder')
            .height($element.outerHeight())
            .width($element.outerWidth());
        return $placeholder;
    }
    
    function isWithinContainer(x, y) {
        const container = $('#container');
        containerOffset = container.offset();
        
        return (
            x >= containerOffset.left &&
            x <= containerOffset.left + container.outerWidth() &&
            y >= containerOffset.top &&
            y <= containerOffset.top + container.outerHeight()
        );
    }
    
    function getInsertPosition(y) {
        let position = -1;
        const container = $('#container');
        const items = container.find('.stack-item:not(.dragging)').toArray();
        
        for (let i = 0; i < items.length; i++) {
            const $element = $(items[i]);
            const offset = $element.offset();
            const height = $element.outerHeight();
            
            if (y < offset.top + height / 2) {
                position = i;
                break;
            }
        }
        
        if (position === -1) {
            position = items.length;
        }
        
        return position;
    }
    
    
    $(document).on('mousedown', '.stack-item', function(e) {
        if (draggingElement) return; 
        e.preventDefault();
        
        mouseStartX = e.clientX;
        mouseStartY = e.clientY;
        
        const $this = $(this);
        
        if ($this.parent().attr('id') !== 'container') {
            return;
        }
        
        draggingElement = $this;
        draggingElementOriginalPosition = $this.index();
        
        const offset = $this.offset();
        elementStartX = offset.left;
        elementStartY = offset.top;
        elementWidth = $this.outerWidth();
        elementHeight = $this.outerHeight();
        
        placeholder = createPlaceholder(this);
        $this.after(placeholder);
        
        $this.addClass('dragging')
            .css({
                position: 'absolute',
                top: elementStartY,
                left: elementStartX,
                width: elementWidth,
                height: elementHeight,
                zIndex: 1000
            });
        
        $('body').append($this);
    });
    
    $(document).on('mousemove', function(e) {
        if (!draggingElement) return;
        
        const dx = e.clientX - mouseStartX;
        const dy = e.clientY - mouseStartY;
        
        draggingElement.css({
            top: elementStartY + dy,
            left: elementStartX + dx
        });
        
        const isInContainer = isWithinContainer(e.clientX, e.clientY);
        
        if (isInContainer) {
            if (placeholder.parent().length === 0) {
                placeholder = createPlaceholder(draggingElement);
            }
            
            const insertPosition = getInsertPosition(e.clientY);
            const $items = $('#container .stack-item:not(.dragging)');
            
            if (insertPosition === 0) {
                $('#container').prepend(placeholder);
            } else if (insertPosition >= $items.length) {
                $('#container').append(placeholder);
            } else {
                $items.eq(insertPosition).before(placeholder);
            }
        } else if (placeholder && placeholder.parent().length > 0) {
            placeholder.detach();
        }
    });
    
    $(document).on('mouseup', function(e) {
        if (!draggingElement) return;
        
        const isInContainer = isWithinContainer(e.clientX, e.clientY);
        
        if (isInContainer && placeholder && placeholder.parent().length > 0) {
            const containerLeft = containerOffset.left;
            const placeholderOffset = placeholder.offset();
            
            draggingElement.css({
                top: placeholderOffset.top,
                left: placeholderOffset.left
            });
            
            placeholder.after(draggingElement);
            placeholder.remove();
            
            draggingElement.removeClass('dragging').removeAttr('style');
            updateItemsListFromDOM(); 
        } else {
            draggingElement.fadeOut(200, function() {
                $(this).remove();
                updateItemsListFromDOM();
            });
            
            if (placeholder) {
                placeholder.remove();
            }
        }
        
        draggingElement = null;
        draggingElementOriginalPosition = null;
        placeholder = null;
    });

    
    $('<button>')
        .text('Add to bottom')
        .css({
            position: 'fixed',
            top: '20px',
            right: '125px',
            padding: '10px',
            backgroundColor: '#2ecc71',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
        })
        .click(function() {
            const itemCount = $('.stack-item').length + 1;
            addItem('Item ' + itemCount);
        })
        .appendTo('body');
    $('<button>')
        .text('Add to top')
        .css({
            position: 'fixed',
            top: '20px',
            right: '20px',
            padding: '10px',
            backgroundColor: '#2ecc71',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
        })
        .click(function() {
            const itemCount = $('.stack-item').length + 1;
            addItem('Item ' + itemCount,0);
        })
        .appendTo('body');
    
    $('<button>')
        .text('Clear All')
        .css({
            position: 'fixed',
            top: '20px',
            right: '250px',
            padding: '10px',
            backgroundColor: '#e74c3c',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
        })
        .click(function() {
            itemsList = [];
            saveToLocalStorage();
            renderItems();
        })
        .appendTo('body');
        
        
    $(document).on('touchstart', '.stack-item', function(e) {
        const touch = e.originalEvent.touches[0];
        const mouseEvent = new MouseEvent('mousedown', {
            clientX: touch.clientX,
            clientY: touch.clientY
        });
        $(this).trigger(mouseEvent);
        e.preventDefault();
    });
    
    $(document).on('touchmove', function(e) {
        if (!draggingElement) return;
        const touch = e.originalEvent.touches[0];
        const mouseEvent = new MouseEvent('mousemove', {
            clientX: touch.clientX,
            clientY: touch.clientY
        });
        $(document).trigger(mouseEvent);
        e.preventDefault();
    });
    
    $(document).on('touchend', function(e) {
        if (!draggingElement) return;
        const mouseEvent = new MouseEvent('mouseup', {});
        $(document).trigger(mouseEvent);
        e.preventDefault();
    });
    
    loadFromLocalStorage();
});