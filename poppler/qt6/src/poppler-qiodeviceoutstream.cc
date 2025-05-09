/* poppler-qiodevicestream.cc: Qt6 interface to poppler
 * Copyright (C) 2008, Pino Toscano <pino@kde.org>
 * Copyright (C) 2013 Adrian Johnson <ajohnson@redneon.com>
 * Copyright (C) 2020, 2021, 2025 Albert Astals Cid <aacid@kde.org>
 * Copyright (C) 2021, Even Rouault <even.rouault@spatialys.com>
 * Copyright (C) 2024, g10 Code GmbH, Author: Sune Stolborg Vuorela <sune@vuorela.dk>
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2, or (at your option)
 * any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street - Fifth Floor, Boston, MA 02110-1301, USA.
 */

#include "poppler-qiodeviceoutstream-private.h"

#include <QtCore/QIODevice>

#include <cstdio>

namespace Poppler {

QIODeviceOutStream::QIODeviceOutStream(QIODevice *device) : m_device(device) { }

QIODeviceOutStream::~QIODeviceOutStream() = default;

void QIODeviceOutStream::close() { }

Goffset QIODeviceOutStream::getPos()
{
    return m_device->pos();
}

void QIODeviceOutStream::put(char c)
{
    m_device->putChar(c);
}

size_t QIODeviceOutStream::write(std::span<const unsigned char> data)
{
    return m_device->write(reinterpret_cast<const char *>(data.data()), data.size());
}

static int poppler_vasprintf(char **buf_ptr, const char *format, va_list ap) GCC_PRINTF_FORMAT(2, 0);

static int poppler_vasprintf(char **buf_ptr, const char *format, va_list ap)
{
    va_list ap_copy;
    va_copy(ap_copy, ap);
    const size_t size = vsnprintf(nullptr, 0, format, ap_copy) + 1;
    va_end(ap_copy);
    *buf_ptr = new char[size];

    return qvsnprintf(*buf_ptr, size, format, ap);
}

void QIODeviceOutStream::printf(const char *format, ...)
{
    va_list ap;
    va_start(ap, format);
    char *buf;
    const size_t bufsize = poppler_vasprintf(&buf, format, ap);
    va_end(ap);
    m_device->write(buf, bufsize);
    delete[] buf;
}

}
